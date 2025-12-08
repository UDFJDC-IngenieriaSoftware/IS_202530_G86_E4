from pydantic import BaseModel
from datetime import datetime


class InvoiceCreate(BaseModel):
    group_id: int
    total_amount: float
    pdf_data: bytes   # ⬅ Guardamos el PDF aquí



class InvoiceOut(InvoiceCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
