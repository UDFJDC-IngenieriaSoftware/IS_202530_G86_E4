from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db
from .schemas import InvoiceCreate, InvoiceOut
from pdf.service import expense_receipt
from .repository import create_invoice, get_invoices_by_group
from groups.repository import get_group_by_id
from expenses.repository import get_expenses_by_group
from users.repository import get_user_by_id



router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/", response_model=InvoiceOut)
def create_invoice_endpoint(data: InvoiceCreate, db: Session = Depends(get_db)):
    return create_invoice(db, data)


@router.get("/{group_id}", response_model=list[InvoiceOut])
def list_group_invoices(group_id: int, db: Session = Depends(get_db)):
    return get_invoices_by_group(db, group_id)


@router.post("/generate/{group_id}", response_model=InvoiceOut)
def generate_invoice(group_id: int, db: Session = Depends(get_db)):
    group = get_group_by_id(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    expenses = get_expenses_by_group(db, group_id)
    if not expenses:
        raise HTTPException(status_code=400, detail="El grupo no tiene gastos")

    created_by = get_user_by_id(db, group.owner_id)
    if not created_by:
        raise HTTPException(status_code=404, detail="Usuario creador no encontrado")

    pdf_bytes, total_expenses = expense_receipt(expenses, group, created_by)

    invoice_data = InvoiceCreate(
        group_id=group.id,
        pdf_file=pdf_bytes,
        total_amount=total_expenses
    )
    invoice_record = create_invoice(db, invoice_data)

    return invoice_record

