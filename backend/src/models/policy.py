from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    roles = relationship("UserRole", back_populates="user")
    policies = relationship("Policy", back_populates="created_by_user")
    policy_versions = relationship("PolicyVersion", back_populates="created_by_user")
    attestations = relationship("Attestation", back_populates="user")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    users = relationship("UserRole", back_populates="role")

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")

class DocumentType(Base):
    __tablename__ = "document_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    policies = relationship("Policy", back_populates="document_type")

class ContentBlob(Base):
    __tablename__ = "content_blobs"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False) # Path to the stored file (e.g., S3 URL, local path)
    file_hash = Column(String, nullable=True) # For integrity check
    size_bytes = Column(Integer, nullable=True)
    mime_type = Column(String, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    policy_versions = relationship("PolicyVersion", back_populates="content_blob")

class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    document_type_id = Column(Integer, ForeignKey("document_types.id"))
    current_version_id = Column(Integer, ForeignKey("policy_versions.id"), nullable=True)
    status = Column(String, default="Draft", nullable=False) # e.g., Draft, In Review, Approved, Published, Archived
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    document_type = relationship("DocumentType", back_populates="policies")
    current_version = relationship("PolicyVersion", foreign_keys=[current_version_id], post_update=True)
    versions = relationship("PolicyVersion", back_populates="policy", foreign_keys="PolicyVersion.policy_id")
    created_by_user = relationship("User", back_populates="policies")
    workflows = relationship("Workflow", back_populates="policy")

class PolicyVersion(Base):
    __tablename__ = "policy_versions"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    effective_date = Column(DateTime(timezone=True), nullable=True)
    content_blob_id = Column(Integer, ForeignKey("content_blobs.id"))
    summary_of_changes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    policy = relationship("Policy", back_populates="versions", foreign_keys=[policy_id])
    search_vector = Column(Text) # PostgreSQL's TSVECTOR type is mapped to Text in SQLAlchemy, but handled by DB-specific functions
    created_by_user = relationship("User", back_populates="policy_versions")
    attestations = relationship("Attestation", back_populates="policy_version")
    review_comments = relationship("ReviewComment", back_populates="policy_version")

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"), nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default="Pending", nullable=False) # e.g., Pending, In Progress, Completed, Cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    policy = relationship("Policy", back_populates="workflows")
    steps = relationship("WorkflowStep", back_populates="workflow")

class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    step_order = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    assigned_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_to_role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    status = Column(String, default="Pending", nullable=False) # e.g., Pending, In Progress, Approved, Rejected, Completed
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    workflow = relationship("Workflow", back_populates="steps")
    assigned_to_user = relationship("User")
    assigned_to_role = relationship("Role")

class Attestation(Base):
    __tablename__ = "attestations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    policy_version_id = Column(Integer, ForeignKey("policy_versions.id"), nullable=False)
    attested_at = Column(DateTime(timezone=True), server_default=func.now())
    signature_data = Column(Text, nullable=True) # e.g., username/password hash, biometric ID

    user = relationship("User", back_populates="attestations")
    policy_version = relationship("PolicyVersion", back_populates="attestations")

class ReviewComment(Base):
    __tablename__ = "review_comments"

    id = Column(Integer, primary_key=True, index=True)
    policy_version_id = Column(Integer, ForeignKey("policy_versions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    policy_version = relationship("PolicyVersion", back_populates="review_comments")
    user = relationship("User")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")