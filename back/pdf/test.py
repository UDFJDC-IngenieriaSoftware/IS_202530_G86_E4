from service import PDFService

class Fake:
    pass

expense = Fake()
expense.title = "Netflix"
expense.amount = 15000
expense.category = "Entretenimiento"
expense.created_at = "2025-12-08"

group = Fake()
group.name = "Grupo Test"

user = Fake()
user.name = "Juan"

participants = [
    {"name": "Juan", "contribution": 7500},
    {"name": "Maria", "contribution": 7500},
]

buffer = PDFService.expense_receipt(expense, group, user, participants)

with open("test.pdf", "wb") as f:
    f.write(buffer.read())
