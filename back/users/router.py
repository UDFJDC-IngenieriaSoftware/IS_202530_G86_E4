from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from users import schemas
from users.repository import get_user_by_email, create_user
from auth.security import hash_password
from auth.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserOut)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user_data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado")
    hashed = hash_password(user_data.password)
    user = create_user(db, email=user_data.email, full_name=user_data.full_name, hashed_password=hashed)
    return user

@router.get("/me", response_model=schemas.UserOut)
def me(current_user = Depends(get_current_user)):
    return current_user
