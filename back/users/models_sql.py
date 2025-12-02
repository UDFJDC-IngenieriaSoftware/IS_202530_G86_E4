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
    expenses_created = relationship("Expense", back_populates="creator")
    expenses_paid = relationship("Expense", back_populates="payer")
    expense_participation = relationship("ExpenseParticipant", back_populates="user")
