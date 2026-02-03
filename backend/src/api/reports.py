from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any

from backend.src.database import get_db
from backend.src.models import policy as models
from backend.src.schemas import policy as schemas
from backend.src.api.auth_api import get_current_active_user, get_current_admin_user, get_current_editor_user

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get("/policy-status-summary", response_model=Dict[str, int])
def get_policy_status_summary(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Only allow admin/editor/reviewer to view this report
    if not any(role.role.name in ["Admin", "Editor", "Reviewer"] for role in current_user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this report")

    summary = db.query(models.Policy.status, func.count(models.Policy.id)).group_by(models.Policy.status).all()
    return {status: count for status, count in summary}

@router.get("/attestation-status/{policy_version_id}", response_model=Dict[str, Any])
def get_attestation_status_for_version(policy_version_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    # Only allow admin/editor/reviewer to view this report
    if not any(role.role.name in ["Admin", "Editor", "Reviewer"] for role in current_user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this report")

    db_policy_version = db.query(models.PolicyVersion).filter(models.PolicyVersion.id == policy_version_id).first()
    if not db_policy_version:
        raise HTTPException(status_code=404, detail="Policy version not found")

    # Get all users (or relevant users, e.g., all active users)
    all_users_count = db.query(models.User).count()
    attested_users = db.query(models.User.username, models.User.email, models.Attestation.attested_at)
    attested_users = attested_users.join(models.Attestation).filter(models.Attestation.policy_version_id == policy_version_id).all()
    
    attested_usernames = {user.username for user, email, attested_at in attested_users}

    non_attested_users = db.query(models.User.username, models.User.email).filter(
        models.User.username.notin_(attested_usernames)
    ).all()

    return {
        "policy_version_id": policy_version_id,
        "policy_title": db_policy_version.policy.title if db_policy_version.policy else 'N/A',
        "version_number": db_policy_version.version_number,
        "total_users": all_users_count,
        "attested_count": len(attested_users),
        "non_attested_count": len(non_attested_users),
        "attested_users": [
            {"username": u, "email": e, "attested_at": t.isoformat()} 
            for u, e, t in attested_users
        ],
        "non_attested_users": [
            {"username": u, "email": e} 
            for u, e in non_attested_users
        ],
    }
