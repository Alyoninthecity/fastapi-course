import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env') #FIXED Relative path for .env
load_dotenv(dotenv_path=dotenv_path) # .env# Carica le variabili d'ambiente

'''
example .env
SECRET_KEY='' #openssl rand -hex 32

DATABASE_URL='postgresql://postgres:1234@localhost/TodoApplicationDatabase'
TEST_DATABASE_URL="postgresql://postgres:1234@localhost/TodoTestApplicationDatabase"
'''


from fastapi import FastAPI, Request, status
from .models import Base
from .database import engine
#Routers
from .routers import auth, todos, admin, user
#HTML
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
app = FastAPI()

Base.metadata.create_all(bind=engine) #Crea tutti i modelli che abbiamo definito con Base nel file models.py
#Dopo puoi fare "sqlite3 todos.db" per usare il db


app.mount("/static", StaticFiles(directory="TodoApp/static"),name="static")

@app.get("/")
def home(request : Request):
    #We need to accept the request that is coming in 
    return RedirectResponse(url="/todos/todo-page",status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def health_check():
    return {'status':'Healthy'}

app.include_router(auth.router) #Incluso il router
app.include_router(todos.router) #Incluso il router
app.include_router(admin.router) #Incluso il router
app.include_router(user.router) #Incluso il router
