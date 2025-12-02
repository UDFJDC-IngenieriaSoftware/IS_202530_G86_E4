from fastapi import FastAPI
from back.database import Base, engine
from auth.router import router as auth_router


from users.models_sql import User
from groups.models_sql import Group, GroupMember
from expenses.models_sql import Expense, ExpenseParticipant
from payments.models_sql import Payment

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Bienvenido a DiviPay API 🚀"}
