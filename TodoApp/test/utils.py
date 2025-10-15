import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__),'..', '.env') #FIXED Relative path for .env
load_dotenv(dotenv_path=dotenv_path) # .env# Carica le variabili d'ambiente

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
import pytest
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
from ..models import Todo, User
from ..routers.auth import bcrypt_context

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

client = TestClient(app)


@pytest.fixture
def test_user():
    user = User(
        email="email@",
        username="admin",
        first_name="admin",
        last_name="admin",
        hashed_password=bcrypt_context.hash("admin"),
        role="admin",
        phone_number="312313",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    # 2. Dopo che il test ha usato la fixture, esegue questo blocco:
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM "user";'))
        connection.execute(text("ALTER SEQUENCE user_id_seq RESTART WITH 1;")) #Postgresql non resetta la sequenza
        connection.commit()
    
@pytest.fixture
def test_todo(test_user):
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
    # 2. Dopo che il test ha usato la fixture, esegue questo blocco:
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todo;"))
        connection.execute(text("ALTER SEQUENCE todo_id_seq RESTART WITH 1;")) #Postgresql non resetta la sequenza
        connection.commit()
