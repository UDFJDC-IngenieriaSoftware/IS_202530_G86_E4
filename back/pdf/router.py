from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db

from expenses.repository import get_expense_by_id, get_expense_participants
from groups.repository import get_group_by_id
from users.repository import get_user_by_id

from pdf.service import PDFService

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/{expense_id}/pdf")
def get_expense_pdf(expense_id: int, db: Session = Depends(get_db)):

    expense = get_expense_by_id(db, expense_id)
    group = get_group_by_id(db, expense.group_id)
    user = get_user_by_id(db, expense.user_id)

    participants = get_expense_participants(db, expense_id)

    participants_data = [
        {
            "name": p.user.name,
            "contribution": p.amount
        }
        for p in participants
    ]

    pdf_buffer = PDFService.expense_receipt(
        expense, group, user, participants_data
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=gasto_{expense_id}.pdf"}
    )
