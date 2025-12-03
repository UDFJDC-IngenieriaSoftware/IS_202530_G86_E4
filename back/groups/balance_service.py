from expenses.models_sql import Expense, ExpenseParticipant
from payments.models_sql import Payment
from sqlalchemy.orm import Session

#Balance del de forma individual
def get_individual_balances(db: Session, group_id: int):

    balances = {}  #user_id: balance_number

    #Sumar lo que pagó cada usuario 
    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
    for e in expenses:
        balances.setdefault(e.paid_by, 0)
        balances[e.paid_by] += e.amount_total

    #Restar lo que debía cada usuario
    participants = db.query(ExpenseParticipant).join(Expense).filter(
        Expense.group_id == group_id
    )
    for p in participants:
        balances.setdefault(p.user_id, 0)
        balances[p.user_id] -= p.amount_owed

    #Aplicar pagos manuales
    payments = db.query(Payment).filter(Payment.group_id == group_id).all()
    for pay in payments:
        balances.setdefault(pay.from_user_id, 0)
        balances.setdefault(pay.to_user_id, 0)
        balances[pay.from_user_id] -= pay.amount
        balances[pay.to_user_id] += pay.amount

    return balances


def simplify_balances(balances: dict):
    debtors = []     # Usuarios que deben dinero (<0)
    creditors = []   # Usuarios a quienes deben dinero (>0)

    for user, bal in balances.items():
        if bal < 0:
            debtors.append([user, -bal])  # Cantidad positiva
        elif bal > 0:
            creditors.append([user, bal])

    result = []

    i = j = 0
    while i < len(debtors) and j < len(creditors):
        debtor_id, debt_amount = debtors[i]
        creditor_id, cred_amount = creditors[j]

        amount = min(debt_amount, cred_amount)

        result.append({
            "from": debtor_id,
            "to": creditor_id,
            "amount": round(amount, 2)
        })

        debtors[i][1] -= amount
        creditors[j][1] -= amount

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return result
