from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class DocumentTypeBase(BaseModel):
    name: str = Field(..., example="Standard Operating Procedure")
    description: Optional[str] = Field(None, example="A formal document outlining procedures.")

class DocumentTypeCreate(DocumentTypeBase):
    pass

class DocumentType(DocumentTypeBase):
    id: int

    class Config:
        orm_mode = True

class ContentBlobBase(BaseModel):
    file_path: str = Field(..., example="/path/to/policy.pdf")
    file_hash: Optional[str] = Field(None, example="a1b2c3d4e5f6g7h8i9j0")
    size_bytes: Optional[int] = Field(None, example=102400)
    mime_type: Optional[str] = Field(None, example="application/pdf")

class ContentBlobCreate(ContentBlobBase):
    pass

class ContentBlob(ContentBlobBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True

class PolicyVersionBase(BaseModel):
    version_number: int = Field(..., example=1)
    effective_date: Optional[datetime] = None
    summary_of_changes: Optional[str] = Field(None, example="Initial draft of the policy.")
    content_blob_id: Optional[int] = None

class PolicyVersionCreate(PolicyVersionBase):
    pass

class PolicyVersion(PolicyVersionBase):
    id: int
    policy_id: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

class PolicyBase(BaseModel):
    title: str = Field(..., example="Employee Handbook")
    description: Optional[str] = Field(None, example="Comprehensive guide for all employees.")
    document_type_id: Optional[int] = None
    status: str = Field("Draft", example="Draft")

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(PolicyBase):
    title: Optional[str] = None
    description: Optional[str] = None
    document_type_id: Optional[int] = None
    status: Optional[str] = None
    current_version_id: Optional[int] = None

class Policy(PolicyBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime
    current_version_id: Optional[int] = None

    document_type: Optional[DocumentType] = None
    current_version: Optional[PolicyVersion] = None
    versions: List[PolicyVersion] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True

class AttestationBase(BaseModel):
    signature_data: Optional[str] = None

class AttestationCreate(AttestationBase):
    user_id: int
    policy_version_id: int

class Attestation(AttestationBase):
    id: int
    user_id: int
    policy_version_id: int
    attested_at: datetime

    class Config:
        orm_mode = True

class WorkflowBase(BaseModel):
    policy_id: int
    name: str = Field(..., example="Policy Review Workflow")
    status: str = Field("Pending", example="Pending")

class WorkflowCreate(WorkflowBase):
    pass

class Workflow(WorkflowBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class WorkflowStepBase(BaseModel):
    workflow_id: int
    step_order: int = Field(..., example=1)
    name: str = Field(..., example="Initial Review")
    assigned_to_user_id: Optional[int] = None
    assigned_to_role_id: Optional[int] = None
    status: str = Field("Pending", example="Pending")
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class WorkflowStepCreate(WorkflowStepBase):
    pass

class WorkflowStep(WorkflowStepBase):
    id: int

    class Config:
        orm_mode = True

class AttestationBase(BaseModel):
    signature_data: Optional[str] = None

class AttestationCreate(AttestationBase):
    user_id: int
    policy_version_id: int

class Attestation(AttestationBase):
    id: int
    user_id: int
    policy_version_id: int
    attested_at: datetime

    class Config:
        orm_mode = True
class NotificationBase(BaseModel):
    user_id: int
    message: str
    read: bool = False

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    read: bool

class Notification(NotificationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
class ReviewCommentBase(BaseModel):
    policy_version_id: int
    user_id: int
    comment_text: str

class ReviewCommentCreate(ReviewCommentBase):
    pass

class ReviewComment(ReviewCommentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True