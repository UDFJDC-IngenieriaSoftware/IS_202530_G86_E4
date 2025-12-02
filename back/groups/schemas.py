from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class GroupCreate(BaseModel):
    name: str

class GroupOut(BaseModel):
    id: int
    name: str
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True

class MemberAdd(BaseModel):
    user_id: int
    role: Optional[str] = "member"

class MemberOut(BaseModel):
    id: int
    user_id: int
    role: str

    class Config:
        orm_mode = True
