from pydantic import BaseModel, Field
from typing import List, Optional

#Los participantes del gasto
class ExpenseParticipantCreate(BaseModel):
    user_id: int
    amount_owed: float = Field(..., ge=0)
    percentage: Optional[float] = None  # si usan división por porcentaje


class ExpenseParticipantOut(BaseModel):
    user_id: int
    amount_owed: float
    percentage: Optional[float]

    class Config:
        orm_mode = True


# El gasto relacionado
class ExpenseCreate(BaseModel):
    title: str
    amount_total: float = Field(..., gt=0)
    paid_by: int
    participants: List[ExpenseParticipantCreate]


class ExpenseOut(BaseModel):
    id: int
    title: str
    amount_total: float
    group_id: int
    created_by: int
    paid_by: int
    participants: List[ExpenseParticipantOut]

    class Config:
        orm_mode = True
