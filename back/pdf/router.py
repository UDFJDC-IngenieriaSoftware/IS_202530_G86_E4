from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db

from expenses.repository import get_expense_by_id, get_expense_participants
from groups.repository import get_group
from users.repository import get_user_by_id

from pdf.service import PDFService

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/{expense_id}/pdf")
def get_expense_pdf(expense_id: int, db: Session = Depends(get_db)):
    
    # Get expense
    expense = get_expense_by_id(db, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    
    # Get group
    group = get_group(db, expense.group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    
    # Get creator user
    user = get_user_by_id(db, expense.created_by)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Get participants
    participants = get_expense_participants(db, expense_id)

    participants_data = [
        {
            "name": p.user.full_name if p.user else f"Usuario #{p.user_id}",
            "contribution": p.amount_owed
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
