from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.src.api.auth_api import get_current_active_user, get_current_admin_user, get_current_editor_user, get_current_reviewer_user
from backend.src.models.policy import Notification as NotificationModel # Alias to avoid conflict
from backend.src.models import policy as models
from backend.src.schemas import policy as schemas
from backend.src.api.auth_api import get_current_active_user, get_current_admin_user, get_current_editor_user, get_current_reviewer_user

router = APIRouter(
    prefix="/workflows",
    tags=["Workflows & Attestations"]
)

# --- Workflow CRUD ---

@router.post("/", response_model=schemas.Workflow, status_code=status.HTTP_201_CREATED)
def create_workflow(workflow: schemas.WorkflowCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_editor_user)):
    db_policy = db.query(models.Policy).filter(models.Policy.id == workflow.policy_id).first()
    if not db_policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    db_workflow = models.Workflow(**workflow.dict())
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow

@router.get("/", response_model=List[schemas.Workflow])
def read_workflows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    workflows = db.query(models.Workflow).offset(skip).limit(limit).all()
    return workflows

@router.get("/{workflow_id}", response_model=schemas.Workflow)
def read_workflow(workflow_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_workflow = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if db_workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return db_workflow

# --- Workflow Step CRUD ---

@router.post("/{workflow_id}/steps/", response_model=schemas.WorkflowStep, status_code=status.HTTP_201_CREATED)
def create_workflow_step(workflow_id: int, step: schemas.WorkflowStepCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_editor_user)):
    db_workflow = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    db_workflow_step = models.WorkflowStep(**step.dict(), workflow_id=workflow_id)
    db.add(db_workflow_step)
    db.commit()
    db.refresh(db_workflow_step)
    return db_workflow_step

@router.get("/{workflow_id}/steps/", response_model=List[schemas.WorkflowStep])
def read_workflow_steps(workflow_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    steps = db.query(models.WorkflowStep).filter(models.WorkflowStep.workflow_id == workflow_id).offset(skip).limit(limit).all()
    return steps

# --- Attestation CRUD ---

@router.post("/attestations/", response_model=schemas.Attestation, status_code=status.HTTP_201_CREATED)
def create_attestation(attestation: schemas.AttestationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    if attestation.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create attestation for another user")

    db_policy_version = db.query(models.PolicyVersion).filter(models.PolicyVersion.id == attestation.policy_version_id).first()
    if not db_policy_version:
        raise HTTPException(status_code=404, detail="Policy version not found")
    
    # Check if user has already attested to this version
    existing_attestation = db.query(models.Attestation).filter(
        models.Attestation.user_id == current_user.id,
        models.Attestation.policy_version_id == attestation.policy_version_id
    ).first()
    if existing_attestation:
        raise HTTPException(status_code=409, detail="User has already attested to this policy version")
    db.refresh(db_attestation)

    # Create a notification for the user who attested
    db_notification = NotificationModel(user_id=current_user.id, message=f"You have successfully attested to policy version {db_policy_version.version_number} of '{db_policy_version.policy.title}'.")
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_attestation
    db_attestation = models.Attestation(**attestation.dict())
    db.add(db_attestation)
    db.commit()
    db.refresh(db_attestation)
    return db_attestation

@router.get("/attestations/policy-version/{policy_version_id}", response_model=List[schemas.Attestation])
def read_attestations_for_version(policy_version_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Only admin/editor/reviewer should see all attestations
    # Regular users should only see their own, but for MVP we allow active user to view
    attestations = db.query(models.Attestation).filter(models.Attestation.policy_version_id == policy_version_id).offset(skip).limit(limit).all()
    return attestations

@router.get("/attestations/{attestation_id}", response_model=schemas.Attestation)
def read_attestation(attestation_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_attestation = db.query(models.Attestation).filter(models.Attestation.id == attestation_id).first()
    if db_attestation is None:
        raise HTTPException(status_code=404, detail="Attestation not found")
    # Ensure user can only view their own attestation unless they are admin/editor/reviewer
    if db_attestation.user_id != current_user.id and not any(role.role.name in ["Admin", "Editor", "Reviewer"] for role in current_user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this attestation")
    return db_attestation

# --- Review Comment CRUD ---

@router.post("/review-comments/", response_model=schemas.ReviewComment, status_code=status.HTTP_201_CREATED)
def create_review_comment(comment: schemas.ReviewCommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_reviewer_user)):
    db_policy_version = db.query(models.PolicyVersion).filter(models.PolicyVersion.id == comment.policy_version_id).first()
    if not db_policy_version:
        raise HTTPException(status_code=404, detail="Policy version not found")

    db_comment = models.ReviewComment(**comment.dict(), user_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/review-comments/policy-version/{policy_version_id}", response_model=List[schemas.ReviewComment])
def read_review_comments_for_version(policy_version_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_reviewer_user)):
    comments = db.query(models.ReviewComment).filter(models.ReviewComment.policy_version_id == policy_version_id).offset(skip).limit(limit).all()
    return comments
