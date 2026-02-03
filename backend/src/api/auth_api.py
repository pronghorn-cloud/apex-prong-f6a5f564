from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from backend.src.database import get_db
from backend.src.models import policy as models
from backend.src.schemas import policy as schemas
from backend.src.auth.auth import verify_password, create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = "8V3B8lKjP0qR2sT4uX6yZ8!A@b#c$d%e^f&g*h(i)j_k+l=m-n.o/p~`" # TODO: Load from environment variable
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    user_id: int = payload.get("id")
    if username is None or user_id is None:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    # Add checks for active status if applicable
    return current_user

async def get_current_admin_user(current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
    if not admin_role:
        raise HTTPException(status_code=500, detail="Admin role not defined")
    user_has_admin_role = db.query(models.UserRole).filter(
        models.UserRole.user_id == current_user.id,
        models.UserRole.role_id == admin_role.id
    ).first()
    if not user_has_admin_role:
async def get_current_editor_user(current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    editor_role = db.query(models.Role).filter(models.Role.name == "Editor").first()
    admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
    if not editor_role or not admin_role:
        raise HTTPException(status_code=500, detail="Editor or Admin role not defined")
    
    is_editor = db.query(models.UserRole).filter(
        models.UserRole.user_id == current_user.id,
        models.UserRole.role_id == editor_role.id
    ).first()
    is_admin = db.query(models.UserRole).filter(
        models.UserRole.user_id == current_user.id,
        models.UserRole.role_id == admin_role.id
    ).first()

    if not is_editor and not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions (requires Editor or Admin role)")
    return current_user

async def get_current_reviewer_user(current_user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    reviewer_role = db.query(models.Role).filter(models.Role.name == "Reviewer").first()
    editor_role = db.query(models.Role).filter(models.Role.name == "Editor").first()
    admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
    if not reviewer_role or not editor_role or not admin_role:
        raise HTTPException(status_code=500, detail="Reviewer, Editor, or Admin role not defined")
    
    is_reviewer = db.query(models.UserRole).filter(
        models.UserRole.user_id == current_user.id,
        models.UserRole.role_id == reviewer_role.id
    ).first()
    is_editor = db.query(models.UserRole).filter(
        models.UserRole.user_id == current_user.id,
        models.UserRole.role_id == editor_role.id
    ).first()
    is_admin = db.query(models.UserRole).filter(
        models.UserRole.user_id == current_user.id,
        models.UserRole.role_id == admin_role.id
    ).first()

    if not is_reviewer and not is_editor and not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions (requires Reviewer, Editor, or Admin role)")
    return current_user
    return current_user
