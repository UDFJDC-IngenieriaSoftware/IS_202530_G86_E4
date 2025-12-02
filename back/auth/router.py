from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from users.repository import get_user_by_email
from auth.security import verify_password, create_access_token
from users.models import UserLogin
from database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}
