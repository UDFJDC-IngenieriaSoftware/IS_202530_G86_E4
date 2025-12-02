from fastapi import FastAPI
from database import Base, engine, get_db


# Modelos para creacion de tablas
from users.models_sql import User
from groups.models_sql import Group, GroupMember
from expenses.models_sql import Expense, ExpenseParticipant
from payments.models_sql import Payment

#Routers para los endpoint de cada clase
from auth.router import router as auth_router  # tu router de login existente
from users.router import router as users_router
from groups.router import router as groups_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(groups_router)

@app.get("/")
def root():
    return {"message": "Bienvenido a DiviPay API 🚀"}
