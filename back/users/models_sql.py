from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relaciones
    groups_owned = relationship("Group", back_populates="owner")
    group_memberships = relationship("GroupMember", back_populates="user")
    expenses_created = relationship("Expense", back_populates="creator", foreign_keys="Expense.created_by")
    expenses_paid = relationship("Expense", back_populates="payer", foreign_keys="Expense.paid_by")
    expense_participation = relationship("ExpenseParticipant", back_populates="user")
