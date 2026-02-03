from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.src.api.auth_api import get_current_active_user, get_current_admin_user, get_current_editor_user, get_current_reviewer_user
from backend.src.api.auth_api import get_current_active_user, get_current_admin_user, get_current_editor_user, get_current_reviewer_user
from backend.src.models.policy import Notification as NotificationModel # Alias to avoid conflict
from backend.src.database import get_db
from backend.src.models import policy as models
from backend.src.schemas import policy as schemas
from backend.src.api.auth_api import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/policies",
    tags=["Policies"]
)
def create_document_type(doc_type: schemas.DocumentTypeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin_user)):
# --- Document Types CRUD ---

@router.post("/document-types/", response_model=schemas.DocumentType, status_code=status.HTTP_201_CREATED)
def create_document_type(doc_type: schemas.DocumentTypeCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin_user)):
    db_doc_type = db.query(models.DocumentType).filter(models.DocumentType.name == doc_type.name).first()
    if db_doc_type:
        raise HTTPException(status_code=400, detail="Document type with this name already exists")
    db_doc_type = models.DocumentType(name=doc_type.name, description=doc_type.description)
    db.add(db_doc_type)
def create_content_blob(content_blob: schemas.ContentBlobCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db.refresh(db_doc_type)
    return db_doc_type

@router.get("/document-types/", response_model=List[schemas.DocumentType])
def read_document_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    doc_types = db.query(models.DocumentType).offset(skip).limit(limit).all()
    return doc_types

@router.get("/document-types/{doc_type_id}", response_model=schemas.DocumentType)
def read_document_type(doc_type_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_doc_type = db.query(models.DocumentType).filter(models.DocumentType.id == doc_type_id).first()
    if db_doc_type is None:
        raise HTTPException(status_code=404, detail="Document type not found")
    return db_doc_type
def create_policy(policy: schemas.PolicyCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_editor_user)):
# --- Content Blobs CRUD (Simplified for MVP) ---

@router.post("/content-blobs/", response_model=schemas.ContentBlob, status_code=status.HTTP_201_CREATED)
def create_content_blob(content_blob: schemas.ContentBlobCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # In a real application, file upload logic would be here.
    # For MVP, we're just storing the path and metadata.
    db_content_blob = models.ContentBlob(**content_blob.dict())
    db.refresh(db_policy)

    # Create a notification for the creator
    db_notification = NotificationModel(user_id=current_user.id, message=f"You created a new policy: {db_policy.title}")
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_policy
    db.commit()
    db.refresh(db_content_blob)
    return db_content_blob

@router.get("/content-blobs/{content_blob_id}", response_model=schemas.ContentBlob)
def read_content_blob(content_blob_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
def update_policy(policy_id: int, policy_update: schemas.PolicyUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_editor_user)):
    if db_content_blob is None:
        raise HTTPException(status_code=404, detail="Content blob not found")
    return db_content_blob

# --- Policies CRUD ---

@router.post("/", response_model=schemas.Policy, status_code=status.HTTP_201_CREATED)
def create_policy(policy: schemas.PolicyCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_policy = models.Policy(**policy.dict(), created_by=current_user.id)
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy

@router.get("/", response_model=List[schemas.Policy])
def read_policies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    policies = db.query(models.Policy).offset(skip).limit(limit).all()
    return policies

@router.get("/{policy_id}", response_model=schemas.Policy)
def read_policy(policy_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    current_user: models.User = Depends(get_current_editor_user)
    if db_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return db_policy

@router.put("/{policy_id}", response_model=schemas.Policy)
def update_policy(policy_id: int, policy_update: schemas.PolicyUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if db_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")

    update_data = policy_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_policy, key, value)

    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy

@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_policy(policy_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin_user)):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if db_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    db.delete(db_policy)
    db.commit()
    return
    db.refresh(db_policy)

    # Create a notification for the policy creator about new version
    db_notification = NotificationModel(user_id=db_policy.created_by, message=f"A new version ({db_policy_version.version_number}) of your policy '{db_policy.title}' has been created.")
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_policy_version
# --- Policy Versions CRUD ---

@router.post("/{policy_id}/versions/", response_model=schemas.PolicyVersion, status_code=status.HTTP_201_CREATED)
def create_policy_version(
    policy_id: int,
    policy_version: schemas.PolicyVersionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if db_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")

    # Determine next version number
    last_version = db.query(models.PolicyVersion).filter(models.PolicyVersion.policy_id == policy_id).order_by(models.PolicyVersion.version_number.desc()).first()
    new_version_number = (last_version.version_number + 1) if last_version else 1

    db_policy_version = models.PolicyVersion(
        **policy_version.dict(),
        policy_id=policy_id,
        version_number=new_version_number,
        created_by=current_user.id
    )
    db.add(db_policy_version)
    db.commit()
    db.refresh(db_policy_version)

    # Update the policy's current_version_id
    db_policy.current_version_id = db_policy_version.id
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)

    return db_policy_version

@router.get("/{policy_id}/versions/", response_model=List[schemas.PolicyVersion])
def read_policy_versions(policy_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    versions = db.query(models.PolicyVersion).filter(models.PolicyVersion.policy_id == policy_id).offset(skip).limit(limit).all()
    return versions

@router.get("/{policy_id}/versions/{version_id}", response_model=schemas.PolicyVersion)
def read_policy_version(policy_id: int, version_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_version = db.query(models.PolicyVersion).filter(
@router.get("/search/", response_model=List[schemas.Policy])
def search_policies(query: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    if not query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    # Use PostgreSQL's full-text search
    search_term = func.plainto_tsquery('english', query)
    policies = db.query(models.Policy).filter(
        models.Policy.search_vector.op('@@')(search_term)
    ).offset(skip).limit(limit).all()
    
    return policies
        models.PolicyVersion.id == version_id
    ).first()
    if db_version is None:
        raise HTTPException(status_code=404, detail="Policy version not found")
    return db_version

    tags=["Policies"]
)

# Helper to get user (placeholder for actual auth)
def get_current_user_id():
    # In a real app, this would come from an authentication token
    return 1 # Assuming admin user for now

# --- Document Types CRUD ---

@router.post("/document-types/", response_model=schemas.DocumentType, status_code=status.HTTP_201_CREATED)
def create_document_type(doc_type: schemas.DocumentTypeCreate, db: Session = Depends(get_db)):
    db_doc_type = models.DocumentType(name=doc_type.name, description=doc_type.description)
    db.add(db_doc_type)
    db.commit()
    db.refresh(db_doc_type)
    return db_doc_type

@router.get("/document-types/", response_model=List[schemas.DocumentType])
def read_document_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    doc_types = db.query(models.DocumentType).offset(skip).limit(limit).all()
    return doc_types

@router.get("/document-types/{doc_type_id}", response_model=schemas.DocumentType)
def read_document_type(doc_type_id: int, db: Session = Depends(get_db)):
    db_doc_type = db.query(models.DocumentType).filter(models.DocumentType.id == doc_type_id).first()
    if db_doc_type is None:
        raise HTTPException(status_code=404, detail="Document type not found")
    return db_doc_type

# --- Content Blobs CRUD (Simplified for MVP) ---

@router.post("/content-blobs/", response_model=schemas.ContentBlob, status_code=status.HTTP_201_CREATED)
def create_content_blob(content_blob: schemas.ContentBlobCreate, db: Session = Depends(get_db)):
    # In a real application, file upload logic would be here.
    # For MVP, we're just storing the path and metadata.
    db_content_blob = models.ContentBlob(**content_blob.dict())
    db.add(db_content_blob)
    db.commit()
    db.refresh(db_content_blob)
    return db_content_blob

@router.get("/content-blobs/{content_blob_id}", response_model=schemas.ContentBlob)
def read_content_blob(content_blob_id: int, db: Session = Depends(get_db)):
    db_content_blob = db.query(models.ContentBlob).filter(models.ContentBlob.id == content_blob_id).first()
    if db_content_blob is None:
        raise HTTPException(status_code=404, detail="Content blob not found")
    return db_content_blob

# --- Policies CRUD ---

@router.post("/", response_model=schemas.Policy, status_code=status.HTTP_201_CREATED)
def create_policy(policy: schemas.PolicyCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    db_policy = models.Policy(**policy.dict(), created_by=current_user_id)
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)

    # Create an initial policy version if content is provided
    if policy.current_version_id: # This is a bit of a hack for initial creation, will be refined
        # For now, current_version_id should be None on creation, versions are added separately
        pass

    return db_policy

@router.get("/", response_model=List[schemas.Policy])
def read_policies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    policies = db.query(models.Policy).offset(skip).limit(limit).all()
    return policies

@router.get("/{policy_id}", response_model=schemas.Policy)
def read_policy(policy_id: int, db: Session = Depends(get_db)):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if db_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    return db_policy

@router.put("/{policy_id}", response_model=schemas.Policy)
def update_policy(policy_id: int, policy_update: schemas.PolicyUpdate, db: Session = Depends(get_db)):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if db_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")

    update_data = policy_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_policy, key, value)

    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy

@router.delete("/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_policy(policy_id: int, db: Session = Depends(get_db)):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if db_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")
    db.delete(db_policy)
    db.commit()
    return

# --- Policy Versions CRUD ---

@router.post("/{policy_id}/versions/", response_model=schemas.PolicyVersion, status_code=status.HTTP_201_CREATED)
def create_policy_version(
    policy_id: int,
    policy_version: schemas.PolicyVersionCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if db_policy is None:
        raise HTTPException(status_code=404, detail="Policy not found")

    # Determine next version number
    last_version = db.query(models.PolicyVersion).filter(models.PolicyVersion.policy_id == policy_id).order_by(models.PolicyVersion.version_number.desc()).first()
    new_version_number = (last_version.version_number + 1) if last_version else 1

    db_policy_version = models.PolicyVersion(
        **policy_version.dict(),
        policy_id=policy_id,
        version_number=new_version_number,
        created_by=current_user_id
    )
    db.add(db_policy_version)
    db.commit()
    db.refresh(db_policy_version)

    # Update the policy's current_version_id
    db_policy.current_version_id = db_policy_version.id
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)

    return db_policy_version

@router.get("/{policy_id}/versions/", response_model=List[schemas.PolicyVersion])
def read_policy_versions(policy_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    versions = db.query(models.PolicyVersion).filter(models.PolicyVersion.policy_id == policy_id).offset(skip).limit(limit).all()
    return versions

@router.get("/{policy_id}/versions/{version_id}", response_model=schemas.PolicyVersion)
def read_policy_version(policy_id: int, version_id: int, db: Session = Depends(get_db)):
    db_version = db.query(models.PolicyVersion).filter(
        models.PolicyVersion.policy_id == policy_id,
        models.PolicyVersion.id == version_id
    ).first()
    if db_version is None:
        raise HTTPException(status_code=404, detail="Policy version not found")
    return db_version
