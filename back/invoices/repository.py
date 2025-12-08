from sqlalchemy.orm import Session
from .models import Invoice
from .schemas import InvoiceCreate


def create_invoice(db: Session, invoice_data: InvoiceCreate):
    invoice = Invoice(
        group_id=invoice_data.group_id,
        total_amount=invoice_data.total_amount,
        pdf_data=invoice_data.pdf_data
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


def get_invoices_by_group(db: Session, group_id: int):
    return db.query(Invoice).filter(Invoice.group_id == group_id).all()
