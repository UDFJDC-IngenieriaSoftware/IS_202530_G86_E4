from sqlalchemy.orm import Session
from payments.models_sql import Payment
from groups.models_sql import GroupMember

from users.repository import get_user_by_id


def user_belongs_to_group(db: Session, user_id: int, group_id: int) -> bool:
    return db.query(GroupMember).filter(
        GroupMember.user_id == user_id,
        GroupMember.group_id == group_id
    ).first() is not None


def create_payment(db: Session, payment_data, group_id: int, current_user_id: int):
    
    #Validar que el usuario destino exista
    to_user = get_user_by_id(db, payment_data.to_user_id)
    if not to_user:
        return None, "El usuario destino no existe"
    
    # Validar que el usuario que paga pertenece al grupo
    if not user_belongs_to_group(db, current_user_id, group_id):
        return None, "No perteneces al grupo"
    

    #Validar que el usuario destino pertenece al grupo
    if not user_belongs_to_group(db, payment_data.to_user_id, group_id):
        return None, "El usuario destino no pertenece al grupo"

    #Evitar pagos a sí mismo    
    if payment_data.to_user_id == current_user_id:
        return None, "No puedes pagarte a ti mismo"
    
    #Evitar pagos no validos
    if payment_data.amount <= 0:
        return None, "El monto debe ser mayor a 0"



    payment = Payment(
        from_user_id=current_user_id,
        to_user_id=payment_data.to_user_id,
        amount=payment_data.amount,
        group_id=group_id
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment, None


def get_payments_by_group(db: Session, group_id: int):
    return db.query(Payment).filter(Payment.group_id == group_id).all()
