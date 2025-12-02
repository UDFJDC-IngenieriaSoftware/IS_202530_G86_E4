from pydantic import BaseModel, Field
from datetime import datetime


class PaymentCreate(BaseModel):
    to_user_id: int
    amount: float = Field(..., gt=0)


class PaymentOut(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    amount: float
    group_id: int
    created_at: datetime

    class Config:
        orm_mode = True
