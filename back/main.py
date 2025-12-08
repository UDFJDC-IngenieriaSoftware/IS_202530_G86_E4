from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

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
from expenses.router import router as expenses_router
from pdf.router import router as pdf_router
from invoices.router import router as invoices_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(groups_router)
app.include_router(expenses_router)
app.include_router(pdf_router)
app.include_router(invoices_router)

# Servir archivos estáticos del frontend
FRONTEND_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "front")

# Montar carpetas especificas para que los links relativos funcionen desde /
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_PATH, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_PATH, "js")), name="js")
# Tambien mantenemos /front por si acaso
app.mount("/front", StaticFiles(directory=FRONTEND_PATH), name="front")

@app.get("/")
def root():
    response = FileResponse(os.path.join(FRONTEND_PATH, "index.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.get("/login.html")
def login_page():
    return FileResponse(os.path.join(FRONTEND_PATH, "login.html"))

@app.get("/dashboard.html")
def dashboard():
    return FileResponse(os.path.join(FRONTEND_PATH, "dashboard.html"))

@app.get("/group.html")
def group():
    return FileResponse(os.path.join(FRONTEND_PATH, "group.html"))
