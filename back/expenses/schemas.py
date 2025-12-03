from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

#Dividir los gastos
class SplitMethod(str, Enum):
    equal = "equal"
    percentage = "percentage"
    manual = "manual"

#Los participantes del gasto
class ExpenseParticipantCreate(BaseModel):
    user_id: int
    amount_owed: Optional[float] = None
    percentage: Optional[float] = None  # si usan división por porcentaje


class ExpenseParticipantOut(BaseModel):
    user_id: int
    amount_owed: float
    percentage: Optional[float]
    participant_name: str = None

    class Config:
        orm_mode = True


# El gasto relacionado
class ExpenseCreate(BaseModel):
    title: str
    amount_total: float
    paid_by: int
    split_method: SplitMethod = SplitMethod.equal
    participants: List[ExpenseParticipantCreate]



class ExpenseOut(BaseModel):
    id: int
    title: str
    amount_total: float
    group_id: int
    created_by: int
    created_at: str = None
    paid_by: int
    payer_name: str = None
    creator_name: str = None
    participants: List[ExpenseParticipantOut]

    class Config:
        orm_mode = True
