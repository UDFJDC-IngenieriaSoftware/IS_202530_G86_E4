from sqlalchemy.orm import Session
from expenses.models_sql import Expense, ExpenseParticipant
from groups.models_sql import GroupMember

from expenses.services import calculate_split



def user_belongs_to_group(db: Session, user_id: int, group_id: int) -> bool:
    return db.query(GroupMember).filter(
        GroupMember.user_id == user_id,
        GroupMember.group_id == group_id
    ).first() is not None


def create_expense(db: Session, expense_data, group_id: int, creator_id: int):
    
    #Validar que el creador pertenece al grupo
    if not user_belongs_to_group(db, creator_id, group_id):
        return None, "El creador no pertenece al grupo"

    #Validar que quien paga pertenece al grupo
    if not user_belongs_to_group(db, expense_data.paid_by, group_id):
        return None, "El usuario que paga no pertenece al grupo"

    #Calcular la división para cada usuario
    try:
        participants = calculate_split(expense_data)
    except ValueError as e:
        return None, str(e)

    #Crear gasto base
    expense = Expense(
        title=expense_data.title,
        amount_total=expense_data.amount_total,
        created_by=creator_id,
        paid_by=expense_data.paid_by,
        group_id=group_id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    #Crear participantes
    for participant in participants:
        if not user_belongs_to_group(db, participant.user_id, group_id):
            return None, f"El usuario {participant.user_id} no pertenece al grupo"

        ep = ExpenseParticipant(
            expense_id=expense.id,
            user_id=participant.user_id,
            amount_owed=participant.amount_owed,
            percentage=participant.percentage
        )
        db.add(ep)

    db.commit()

    return expense, None


def get_expenses_by_group(db: Session, group_id: int):
    return db.query(Expense).filter(Expense.group_id == group_id).all()


def get_expense_detail(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()
