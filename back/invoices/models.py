from sqlalchemy import Column, Integer, ForeignKey, LargeBinary, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    pdf_data = Column(LargeBinary, nullable=False)  # ⬅ Aquí va el PDF
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    group = relationship("Group")
