from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.src.database import get_db
from backend.src.models import policy as models
from backend.src.schemas import policy as schemas
from backend.src.api.auth_api import get_current_active_user, get_current_admin_user

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.post("/", response_model=schemas.Notification, status_code=status.HTTP_201_CREATED)
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_admin_user)):
    # Only admin can create notifications for any user for now, or internal system
    db_notification = models.Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.get("/me/", response_model=List[schemas.Notification])
def get_my_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    notifications = db.query(models.Notification).filter(models.Notification.user_id == current_user.id).offset(skip).limit(limit).all()
    return notifications

@router.put("/{notification_id}/read", response_model=schemas.Notification)
def mark_notification_as_read(notification_id: int, update: schemas.NotificationUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if db_notification.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this notification")
    
    db_notification.read = update.read
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if db_notification.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this notification")
    
    db.delete(db_notification)
    db.commit()
    return
