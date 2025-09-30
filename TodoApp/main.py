from fastapi import FastAPI
import models
from database import engine
#Routers
from routers import auth, todos, admin

app = FastAPI()

models.Base.metadata.create_all(bind=engine) #Crea tutti i modelli che abbiamo definito con Base nel file models.py
#Dopo puoi fare "sqlite3 todos.db" per usare il db

app.include_router(auth.router) #Incluso il router
app.include_router(todos.router) #Incluso il router
app.include_router(admin.router) #Incluso il router
