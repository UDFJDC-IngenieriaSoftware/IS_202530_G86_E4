from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from auth.deps import get_current_user

from expenses.repository import (
    create_expense,
    get_expenses_by_group,
    get_expense_detail
)

router = APIRouter(
    prefix="/groups/{group_id}/expenses",
    tags=["expenses"]
)


@router.post("/")
def create_expense_route(
    group_id: int,
    expense_data,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    expense, error = create_expense(db, expense_data, group_id, current_user.id)

    if error:
        raise HTTPException(status_code=400, detail=error)

    return expense


@router.get("/")
def list_expenses_route(
    group_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    expenses = get_expenses_by_group(db, group_id)
    return expenses


@router.get("/{expense_id}")
def get_expense_route(
    group_id: int,
    expense_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    expense = get_expense_detail(db, expense_id)

    if not expense or expense.group_id != group_id:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")

    return expense
