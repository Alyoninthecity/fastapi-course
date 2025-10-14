from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import SessionLocal


def get_db():
    '''
    Utilizzando yield non devo chiudere la connessione db ogni volta che ottengo il db quindi chiude la connessione in automatico quando finisce
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Dependency Injection
db_dependency=Annotated[Session,Depends(get_db)]