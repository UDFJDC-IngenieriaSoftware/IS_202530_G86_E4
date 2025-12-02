from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    paid_by = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    amount_total = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    group = relationship("Group", back_populates="expenses")
    creator = relationship("User", back_populates="expenses_created", foreign_keys=[created_by])
    payer = relationship("User", back_populates="expenses_paid", foreign_keys=[paid_by])
    participants = relationship("ExpenseParticipant", back_populates="expense", cascade="all, delete")

class ExpenseParticipant(Base):
    __tablename__ = "expense_participants"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    amount_owed = Column(Float, nullable=False)
    percentage = Column(Float)  # opcional

    # Relaciones
    expense = relationship("Expense", back_populates="participants")
    user = relationship("User", back_populates="expense_participation")
