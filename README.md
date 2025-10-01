# (English) - FastAPI Course Project - Documentation and Workflow

## General Architecture

This codebase contains multiple FastAPI projects:

- **TodoApp**: Main application for todo management, JWT authentication, users and roles.
- **books.py / books2.py**: Example APIs for books, with validation, CRUD, path/query params.

## Key Components

- `TodoApp/`
  - `main.py`: FastAPI entry point, includes `auth` and `todos` routers. Creates DB models at startup.
  - `database.py`: SQLite3 setup and connection (`todosapp.db`). Exposes `SessionLocal` and `Base` for SQLAlchemy.
  - `models.py`: ORM models (User, Todo) with SQLAlchemy.
  - `dependencies.py`: Dependency injection for DB session (`get_db`, `db_dependency`).
  - `routers/`
    - `auth.py`: JWT authentication API, user creation, login, password hashing (`passlib`, `bcrypt`).
    - `todos.py`: Todo CRUD API, validation, error handling.
  - `run.py`: Script to launch the app with uvicorn.
  - `usare_sqlite3.md`: Useful commands for working with SQLite3.
- `books.py`, `books2.py`: Example APIs for books, with validation, path/query params, CRUD methods, status codes, and error handling.
- `run_book.py`, `run_book2.py`, `run_TodoApp.py`: Scripts to launch the respective apps with uvicorn.

## Development Commands & Workflow

- **All pip install:**

  ```
  pip install fastapi
  pip install "uvicorn[fastapi]"
  pip install sqlalchemy
  pip install passlib
  pip install bcrypt==4.0.1
  pip install python-multipart
  pip install "python-jose[cryptography]"
  pip install python-dotenv
  pip install psycopg2-binary
  pip install alembic
  ```
- **Start TodoApp:**

  ```sh
  cd ./TodoApp
  uvicorn main:app --reload
  ```
- **Start books.py/books2.py:**

  ```sh
  python run_book.py   # books.py
  python run_book2.py  # books2.py
  python run_TodoApp.py # TodoApp
  ```
- **Kill processes on port 8000 (Windows):**

  ```sh
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```
- **Install main dependencies:**

  ```sh
  pip install -r requirements.txt
  pip install python-multipart
  pip install "python-jose[cryptography]"
  pip install passlib bcrypt==4.0.1
  pip install python-dotenv
  ```
- **Useful SQLite commands:**

  ```sql
  sqlite3 todosapp.db
  .schema
  .mode table
  select * from user;
  select * from todo;
  .quit
  ```
- **Swagger UI:** Go to `/docs` after starting the server.

## Alembic
- alembic init <folder> - Initialized a new, generic env
- alembic revision -m <message> - Creates a new revision of the env (all db scripts to change and migrate the db)
- alembic upgrade <revision #> - Run our upgrade migration to our db
- alembic downgrade -1 - Downgrade migration to our db
##### Alembic.ini - All configurations
- sqlalchemy.url = driver://user:pass@localhost/dbname
##### Alembic directory
## Conventions & Patterns

- All APIs are organized in routers and registered in `main.py`.
- The DB is SQLite3 (`todosapp.db`), accessed via dependency injection.
- JWT: key generated with `openssl rand -hex 32`, HS256 algorithm, managed in `auth.py`.
- Data validation: Pydantic (request/response models).
- ORM: SQLAlchemy, models in `models.py`.
- HTTP errors handled with `HTTPException` and explicit status codes.
- Examples of status codes and advanced validation in `books2.py`.

## Implementation Examples

- **Add a new router:**
  1. Create a file in `TodoApp/routers/` (e.g. `myfeature.py`):
     ```python
     from fastapi import APIRouter
     router = APIRouter()

     @router.get("/myfeature")
     async def myfeature():
     return {"msg": "it works!"}
     ```
  2. In `main.py` import and register the router:
     ```python
     from routers import myfeature

     app = FastAPI()
     app.include_router(myfeature.router)
     ```
- **Create a new ORM model:**
  - File: `TodoApp/models.py`
  - Example:
    ```python
    class MyModel(Base):
       	 __tablename__ = 'mytable'
       	 id = Column(Integer, primary_key=True)
       	 # ...
    ```
- **DB dependency injection:**
  - File: `TodoApp/dependencies.py`
  - Example:
    ```python
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from database import SessionLocal

    def get_db():
       	 db = SessionLocal()
       	 try:
       			 yield db
       	 finally:
       			 db.close()
    db_dependency = Annotated[Session, Depends(get_db)]
    ```
- **JWT Authentication:**
  - File: `TodoApp/routers/auth.py`
  - Example:
    ```python
    from jose import jwt
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = 'HS256'
    def createAccessToken(username, user_id, expires_delta):
       	 encode = {'sub': username, 'id': user_id}
       	 # ...
       	 return jwt.encode(encode, SECRET_KEY, ALGORITHM)
    ```
- **Todo CRUD:**
  - File: `TodoApp/routers/todos.py`
  - Example:
    ```python
    @router.post("/todo", status_code=201)
    async def create_todo(db: db_dependency, todo_request: TodoRequest):
       	 todo_model = Todo(**todo_request.model_dump())
       	 db.add(todo_model)
       	 db.commit()
    ```
- **Advanced validation with Pydantic:**
  - File: `books2.py`, `TodoApp/routers/todos.py`
  - Example:
    ```python
    class TodoRequest(BaseModel):
       	 title: str = Field(min_length=3)
       	 description: str = Field(min_length=3, max_length=100)
       	 priority: int = Field(gt=0, lt=6)
       	 complete: bool
    ```
- **HTTP error handling:**
  - File: `TodoApp/routers/todos.py`, `books2.py`
  - Example:
    ```python
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Not found")
    ```
- **Book API example:**
  - File: `books.py`, `books2.py`
  - Example:
    ```python
    @app.get("/books/{book_id}")
    async def read_book_id(book_id: int):
       	 # ...
    ```

## Secure SECRET_KEY Management

- Never write your SECRET_KEY directly in code!
- Use a `.env` file (do NOT commit it) and the `python-dotenv` library:

  1. Create `.env` in the project root:
     ```
     SECRET_KEY=your_secret_key
     ```
  2. Install the library:
     ```sh
     pip install python-dotenv
     ```
  3. Load the variable in Python (e.g. in `auth.py`):
     ```python
     import os
     from dotenv import load_dotenv
     load_dotenv()
     SECRET_KEY = os.getenv("SECRET_KEY")
     ```
- This keeps your key safe and out of version control!

## Import Reference

- `from fastapi import FastAPI, APIRouter, Depends, HTTPException, Path, Body, Query`: FastAPI core imports for app creation, modular routers, dependency injection, error handling, and parameter validation.

  - Example: `app = FastAPI()` in `main.py`, `router = APIRouter()` in `routers/todos.py`
- `from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer`: OAuth2 authentication utilities for login and token management.

  - Example: `oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')` in `routers/auth.py`
- `from starlette import status`: Constants for HTTP status codes (e.g. status.HTTP_201_CREATED).

  - Example: `status.HTTP_200_OK` in `routers/todos.py`
- `from pydantic import BaseModel, Field`: Data validation and serialization (request/response models, field constraints).

  - Example: `class TodoRequest(BaseModel): ...` in `routers/todos.py`
- `from typing import Annotated, Optional`: Type hints for dependency injection and optional fields.

  - Example: `db_dependency = Annotated[Session, Depends(get_db)]` in `dependencies.py`
- `from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine`: SQLAlchemy ORM for table/model definitions and DB engine creation.

  - Example: `class User(Base): ... id = Column(Integer, primary_key=True)` in `models.py`
- `from sqlalchemy.orm import Session, sessionmaker`: SQLAlchemy ORM for DB session management.

  - Example: `SessionLocal = sessionmaker(...)` in `database.py`
- `from sqlalchemy.ext.declarative import declarative_base`: SQLAlchemy ORM base class for models.

  - Example: `Base = declarative_base()` in `database.py`
- `from jose import JWTError, jwt`: JWT encoding/decoding for authentication.

  - Example: `jwt.encode(encode, SECRET_KEY, ALGORITHM)` in `routers/auth.py`
- `from passlib.context import CryptContext`: Password hashing and verification.

  - Example: `bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')` in `routers/auth.py`
- `from datetime import datetime, timedelta, timezone`: Date/time management (token expiry, timestamps).

  - Example: `expires = datetime.now(timezone.utc) + expires_delta` in `routers/auth.py`
- `import os`: Access to environment variables (e.g. SECRET_KEY).

  - Example: `SECRET_KEY = os.getenv("SECRET_KEY")` in `routers/auth.py`
- `from dotenv import load_dotenv`: Load environment variables from .env file.

  - Example: `load_dotenv()` in `routers/auth.py`
- `from models import User, Todo`: Import ORM models for DB operations.

  - Example: `from models import Todo` in `routers/todos.py`
- `from dependencies import db_dependency`: Import DB session dependency for route functions.

  - Example: `async def create_todo(db: db_dependency, ...)` in `routers/todos.py`
- `from database import engine, SessionLocal, Base`: DB engine/session/base for ORM.

  - Example: `models.Base.metadata.create_all(bind=engine)` in `main.py`

# (Italiano) - FastAPI Course Project - Documentation and Workflow

## Architettura Generale

Questa codebase contiene più progetti FastAPI:

- **TodoApp**: Applicazione principale per la gestione di todo, autenticazione JWT, utenti e ruoli.
- **books.py / books2.py**: API di esempio per libri, con validazione, CRUD, path/query params.

## Componenti Chiave

- `TodoApp/`
  - `main.py`: Entry point FastAPI, include i router `auth` e `todos`. Crea i modelli nel DB all'avvio.
  - `database.py`: Setup e connessione SQLite3 (`todosapp.db`). Espone `SessionLocal` e `Base` per SQLAlchemy.
  - `models.py`: Modelli ORM (User, Todo) con SQLAlchemy.
  - `dependencies.py`: Dependency injection per DB session (`get_db`, `db_dependency`).
  - `routers/`
    - `auth.py`: API di autenticazione JWT, creazione utenti, login, hashing password (`passlib`, `bcrypt`).
    - `todos.py`: CRUD Todo, validazione con Pydantic, gestione errori HTTP.
  - `run.py`: Script per avviare l'app con uvicorn.
  - `usare_sqlite3.md`: Comandi utili per lavorare con SQLite3.
- `books.py`, `books2.py`: API di esempio per libri, con validazione, path/query params, metodi CRUD, status code e gestione errori.
- `run_book.py`, `run_book2.py`, `run_TodoApp.py`: Script per avviare le rispettive app con uvicorn.

## Comandi e Workflow Sviluppo

- **Avvia TodoApp :**
  ```sh
  cd ./TodoApp
  uvicorn main:app --reload
  ```
- **Avvia books.py/books2.py:**
  ```sh
  python run_book.py   # books.py
  python run_book2.py  # books2.py
  python run_TodoApp.py # TodoApp
  ```
- **Uccidere processi su porta 8000 (Windows):**
  ```sh
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
  ```
- **Installa dipendenze principali:**
  ```sh
  pip install -r requirements.txt
  pip install python-multipart
  pip install "python-jose[cryptography]"
  pip install passlib bcrypt==4.0.1
  pip install python-dotenv
  ```
- **Comandi SQLite utili:**
  ```sql
  sqlite3 todosapp.db
  .schema
  .mode table
  select * from user;
  select * from todo;
  .quit
  ```
- **Swagger UI:** Vai su `/docs` dopo aver avviato il server.

## Convenzioni e Pattern

- Tutte le API sono organizzate in router e registrate in `main.py`.
- Il DB è SQLite3 (`todosapp.db`), accesso tramite dependency injection.
- JWT: chiave generata con `openssl rand -hex 32`, algoritmo HS256, gestione in `auth.py`.
- Validazione dati: Pydantic (modelli request/response).
- ORM: SQLAlchemy, modelli in `models.py`.
- Errori HTTP gestiti con `HTTPException` e status code espliciti.
- Esempi di status code e validazione avanzata in `books2.py`.

## Esempi di Implementazione

- **Aggiungi un nuovo router:**
  1. Crea un file in `TodoApp/routers/` (es: `myfeature.py`):

     ```python
     python
     from fastapi import APIRouter
     router = APIRouter()

     @router.get("/myfeature")
     async def myfeature():
     return {"msg": "funziona!"}
     ```
  2. In `main.py` importa e registra il router:

     ```python
     from routers import myfeature

     app = FastAPI()
     app.include_router(myfeature.router)
     ```
- **Crea un nuovo modello ORM:**
  - File: `TodoApp/models.py`
  - Esempio:
    ```python
    class MyModel(Base):
       	 __tablename__ = 'mytable'
       	 id = Column(Integer, primary_key=True)
       	 # ...
    ```
- **Dependency injection DB:**
  - File: `TodoApp/dependencies.py`
  - Esempio:
    ```python
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from database import SessionLocal

    def get_db():
       	 db = SessionLocal()
       	 try:
       			 yield db
       	 finally:
       			 db.close()
    db_dependency = Annotated[Session, Depends(get_db)]
    ```
- **Autenticazione JWT:**
  - File: `TodoApp/routers/auth.py`
  - Esempio:
    ```python
    from jose import jwt
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = 'HS256'
    def createAccessToken(username, user_id, expires_delta):
       	 encode = {'sub': username, 'id': user_id}
       	 # ...
       	 return jwt.encode(encode, SECRET_KEY, ALGORITHM)
    ```
- **CRUD Todo:**
  - File: `TodoApp/routers/todos.py`
  - Esempio:
    ```python
    @router.post("/todo", status_code=201)
    async def create_todo(db: db_dependency, todo_request: TodoRequest):
       	 todo_model = Todo(**todo_request.model_dump())
       	 db.add(todo_model)
       	 db.commit()
    ```
- **Validazione avanzata con Pydantic:**
  - File: `books2.py`, `TodoApp/routers/todos.py`
  - Esempio:
    ```python
    class TodoRequest(BaseModel):
       	 title: str = Field(min_length=3)
       	 description: str = Field(min_length=3, max_length=100)
       	 priority: int = Field(gt=0, lt=6)
       	 complete: bool
    ```
- **Gestione errori HTTP:**
  - File: `TodoApp/routers/todos.py`, `books2.py`
  - Esempio:
    ```python
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Non trovato")
    ```
- **Esempio API libri:**
  - File: `books.py`, `books2.py`
  - Esempio:
    ```python
    @app.get("/books/{book_id}")
    async def read_book_id(book_id: int):
       	 # ...
    ```

## Gestione sicura SECRET_KEY

- Non scrivere la SECRET_KEY direttamente nel codice!
- Usa un file `.env` (da NON committare) e la libreria `python-dotenv`:
  1. Crea `.env` nella root:
     ```
     SECRET_KEY=la_tua_secret_key
     ```
  2. Installa la libreria:
     ```sh
     pip install python-dotenv
     ```
  3. Carica la variabile in Python (es. in `auth.py`):
     ```python
     import os
     from dotenv import load_dotenv
     load_dotenv()
     SECRET_KEY = os.getenv("SECRET_KEY")
     ```
- Così la chiave resta sicura e fuori dal versionamento!

## Riferimento Import

- `from fastapi import FastAPI, APIRouter, Depends, HTTPException, Path, Body, Query`: Import principali FastAPI per creazione app, router modulari, dependency injection, gestione errori e validazione parametri.
  - Esempio: `app = FastAPI()` in `main.py`, `router = APIRouter()` in `routers/todos.py`
- `from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer`: Utilità per autenticazione OAuth2 (login, gestione token).
  - Esempio: `oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')` in `routers/auth.py`
- `from starlette import status`: Costanti per status code HTTP (es. status.HTTP_201_CREATED).
  - Esempio: `status.HTTP_200_OK` in `routers/todos.py`
- `from pydantic import BaseModel, Field`: Validazione/serializzazione dati (modelli request/response, vincoli campi).
  - Esempio: `class TodoRequest(BaseModel): ...` in `routers/todos.py`
- `from typing import Annotated, Optional`: Tipizzazione per dependency injection e campi opzionali.
  - Esempio: `db_dependency = Annotated[Session, Depends(get_db)]` in `dependencies.py`
- `from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine`: ORM SQLAlchemy per definizione tabelle/modelli e creazione engine DB.
  - Esempio: `class User(Base): ... id = Column(Integer, primary_key=True)` in `models.py`
- `from sqlalchemy.orm import Session, sessionmaker`: ORM SQLAlchemy per gestione sessioni DB.
  - Esempio: `SessionLocal = sessionmaker(...)` in `database.py`
- `from sqlalchemy.ext.declarative import declarative_base`: Base ORM SQLAlchemy per i modelli.
  - Esempio: `Base = declarative_base()` in `database.py`
- `from jose import JWTError, jwt`: Codifica/decodifica JWT per autenticazione.
  - Esempio: `jwt.encode(encode, SECRET_KEY, ALGORITHM)` in `routers/auth.py`
- `from passlib.context import CryptContext`: Hashing/verifica password.
  - Esempio: `bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')` in `routers/auth.py`
- `from datetime import datetime, timedelta, timezone`: Gestione date/ora (scadenza token, timestamp).
  - Esempio: `expires = datetime.now(timezone.utc) + expires_delta` in `routers/auth.py`
- `import os`: Accesso a variabili d'ambiente (es. SECRET_KEY).
  - Esempio: `SECRET_KEY = os.getenv("SECRET_KEY")` in `routers/auth.py`
- `from dotenv import load_dotenv`: Caricamento variabili da file .env.
  - Esempio: `load_dotenv()` in `routers/auth.py`
- `from models import User, Todo`: Import modelli ORM per operazioni DB.
  - Esempio: `from models import Todo` in `routers/todos.py`
- `from dependencies import db_dependency`: Import della dependency per la sessione DB nelle route.
  - Esempio: `async def create_todo(db: db_dependency, ...)` in `routers/todos.py`
- `from database import engine, SessionLocal, Base`: Engine/session/base per ORM.
  - Esempio: `models.Base.metadata.create_all(bind=engine)` in `main.py`
