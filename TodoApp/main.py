import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env') #FIXED Relative path for .env
load_dotenv(dotenv_path=dotenv_path) # .env# Carica le variabili d'ambiente

from fastapi import FastAPI, Request
from .models import Base
from .database import engine
#Routers
from .routers import auth, todos, admin, user
#HTML
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
app = FastAPI()

Base.metadata.create_all(bind=engine) #Crea tutti i modelli che abbiamo definito con Base nel file models.py
#Dopo puoi fare "sqlite3 todos.db" per usare il db

templates = Jinja2Templates(directory="TodoApp/templates")

app.mount("/static", StaticFiles(directory="TodoApp/static"),name="static")

@app.get("/")
def test(request : Request):
    #We need to accept the request that is coming in 
    return templates.TemplateResponse("login.html",{"request":request})


@app.get("/healthy")
def health_check():
    return {'status':'Healthy'}

app.include_router(auth.router) #Incluso il router
app.include_router(todos.router) #Incluso il router
app.include_router(admin.router) #Incluso il router
app.include_router(user.router) #Incluso il router
