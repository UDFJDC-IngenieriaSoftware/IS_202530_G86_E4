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


from expenses.schemas import ExpenseCreate

@router.post("/")
def create_expense_route(
    group_id: int,
    expense_data: ExpenseCreate,
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
    
    # Add payer names, creator names, and participant names
    from users.repository import get_user_by_id
    result = []
    for e in expenses:
        payer = get_user_by_id(db, e.paid_by)
        creator = get_user_by_id(db, e.created_by)
        
        # Get participant names
        participants_with_names = []
        for p in e.participants:
            participant_user = get_user_by_id(db, p.user_id)
            participants_with_names.append({
                "user_id": p.user_id,
                "amount_owed": p.amount_owed,
                "percentage": p.percentage,
                "participant_name": participant_user.full_name if participant_user else f"User #{p.user_id}"
            })
        
        expense_dict = {
            "id": e.id,
            "title": e.title,
            "amount_total": e.amount_total,
            "group_id": e.group_id,
            "created_by": e.created_by,
            "created_at": e.date.isoformat() if e.date else None,
            "paid_by": e.paid_by,
            "payer_name": payer.full_name if payer else f"User #{e.paid_by}",
            "creator_name": creator.full_name if creator else f"User #{e.created_by}",
            "participants": participants_with_names
        }
        result.append(expense_dict)
    return result


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
