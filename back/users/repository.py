from sqlalchemy.orm import Session
from .models_sql import User

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, full_name: str, hashed_password: str):
    user = User(email=email, full_name=full_name, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
