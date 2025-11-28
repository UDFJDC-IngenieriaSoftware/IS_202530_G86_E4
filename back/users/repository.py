from .models import UserInDB
from auth.security import hash_password

users_db_trial = {
    "user@example.com": UserInDB(
        email="user@example.com",
        hashed_password=hash_password("12345"),
        full_name="User Example"
    )
}

def get_user_by_email(email: str):
    return users_db_trial.get(email)
