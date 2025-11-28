from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    full_name: str
