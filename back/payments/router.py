from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from auth.deps import get_current_user
from payments.repository import create_payment, get_payments_by_group

router = APIRouter(
    prefix="/groups/{group_id}/payments",
    tags=["payments"]
)


@router.post("/")
def create_payment_route(
    group_id: int,
    payment_data,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    payment, error = create_payment(db, payment_data, group_id, current_user.id)

    if error:
        raise HTTPException(status_code=400, detail=error)

    return payment


@router.get("/")
def list_payments_route(
    group_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    payments = get_payments_by_group(db, group_id)
    return payments
