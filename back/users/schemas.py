from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    class Config:
        orm_mode = True
