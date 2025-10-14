import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ..main import app
from ..dependencies import get_db
from ..routers.auth import get_current_user

from fastapi.testclient import TestClient
from fastapi import status

import pytest
from ..models import Todo
dotenv_path = os.path.join(os.path.dirname(__file__),'..', '.env') #FIXED Relative path for .env
load_dotenv(dotenv_path=dotenv_path) # .env# Carica le variabili d'ambiente

SQLALCHEMY_TEST_DATABASE_URL=os.getenv("TEST_DATABASE_URL")

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL,poolclass=StaticPool
    #, connect_args={'check_same_thread':False}
    )

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine) #Crea tutti i modelli che abbiamo definito con Base nel file models.py

def override_get_db():
    '''
    Utilizzando yield non devo chiudere la connessione db ogni volta che ottengo il db quindi chiude la connessione in automatico quando finisce
    '''
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'admin','id':1,'user_role':'admin'}

#Override Dependency Injection for TESTING MOC
app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todo(
        title="Learn to Code",
        description="Need to learn okkk??",
        priority=5,
        complete=False,
        owner=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todo;"))
        connection.execute(text("ALTER SEQUENCE todo_id_seq RESTART WITH 1;")) #Postgresql non resetta la sequenza
        connection.commit()

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code== status.HTTP_200_OK
    assert response.json()== [{'title':"Learn to Code",
                                "description":"Need to learn okkk??",
                                "priority":5,
                                "complete":False,
                                "owner":1,
                                'id':1}
                            ]

def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code== status.HTTP_200_OK
    assert response.json()== {'title':"Learn to Code",
                                "description":"Need to learn okkk??",
                                "priority":5,
                                "complete":False,
                                "owner":1,
                                'id':1}

def test_read_one_authenticated_not_found(test_todo):
    response = client.get("/todo/999")
    assert response.status_code== status.HTTP_404_NOT_FOUND
    assert response.json()== {'detail':'Todo non trovato'}
    
def test_create_todo(test_todo):
    request_data = {
                    'title':"Learn to Code Create",
                    "description":"Need to learn okkk??",
                    "priority":5,
                    "complete":False,
                    }
    response = client.post('/todo/',json=request_data)
    assert response.status_code== status.HTTP_201_CREATED
    
    db = TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id==2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
