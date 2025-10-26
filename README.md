# FastAPI Course Project - Documentation and Workflow

> **Live Demo:** You can test a live version of this application here: **[https://fastapi-course-xevp.onrender.com/todos/todo-page](https://fastapi-course-xevp.onrender.com/todos/todo-page)**
>
> This application is deployed on **Render.com** and the database is hosted on **Neon.com**.

## General Architecture

This repository contains the main project developed during the FastAPI course, a complete web application for "Todo" management with a web interface, user authentication, and a RESTful API.

## ✨ Key Features

* **User Management** : Registration and Login with JWT-based authentication.
* **Todo CRUD** : Create, Read, Update, and Delete personal todos.
* **Web Interface** : Server-side rendered frontend built with Jinja2 templates and Bootstrap.
* **RESTful API** : Documented endpoints (via Swagger UI) to interact with resources via API.
* **User Roles** : Distinction between standard users and administrators (basic logic implemented).
* **Database Migrations** : Database schema management via Alembic.
* **Automated Tests** : Integration test suite with Pytest.

## 🛠️ Tech Stack

* **Backend** : FastAPI
* **Database** : SQLAlchemy (with SQLite)
* **Authentication** : JWT (python-jose), Passlib, Bcrypt
* **Migrations** : Alembic
* **Frontend** : Jinja2, Bootstrap
* **Testing** : Pytest, HTTPX
* **Data Validation** : Pydantic
* **Dependencies** : python-dotenv, python-multipart

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

* Python 3.8+
* A Python package manager (pip)

### 2. Project Setup

1. **Clone the repository:**

   ```
   git clone [https://github.com/Alyoninthecity/fastapi-course.git](https://github.com/Alyoninthecity/fastapi-course.git)
   cd fastapi-course
   ```
2. **Create and activate a virtual environment:**

   ```
   # Windows
   python -m venv fastapienv
   .\fastapienv\Scripts\activate

   # macOS / Linux
   python3 -m venv fastapienv
   source fastapienv/bin/activate
   ```
3. **Install dependencies:**
   All necessary dependencies are listed in the `requirements.txt` file.

   ```
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   The application uses a `.env` file to manage secret keys.
   Create a file named `.env` in the root of the `TodoApp/` folder and add the following variable:

   ```
   # Example for TodoApp/.env
   SECRET_KEY=your_jwt_secret_generated_with_openssl
   ```

   *You can generate a secure key with the command: `openssl rand -hex 32`*
5. **Initialize and update the database:**
   Use Alembic to apply all migrations and create the tables in the SQLite database.

   ```
   # Make sure you are in the project root (where alembic.ini is located)
   alembic upgrade head
   ```

   This command will create a `todosapp.db` file in the `TodoApp/` folder with all the necessary tables.

### 3. Running the Application

To start the development server with hot-reload:

```
uvicorn TodoApp.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

### 4. Running Tests

To run the integration test suite and verify that everything is working correctly:

```
pytest
```

This codebase contains multiple FastAPI projects:

- **TodoApp**: Main application for todo management, JWT authentication, users and roles.
- **books.py / books2.py**: Example APIs for books, with validation, CRUD, path/query params.

## Key Components

- `TodoApp/`
  - `main.py`: FastAPI entry point, includes `auth` and `todos` routers. Creates DB models at startup.
  - `database.py`: Configuration for the database connection (SQLite) and SQLAlchemy session. Exposes `SessionLocal` and `Base` for SQLAlchemy.
  - `models.py`: ORM models (User, Todo) with SQLAlchemy.
  - `dependencies.py`: Dependency injection for DB session (`get_db`, `db_dependency`).
  - `routers/`
    - `auth.py`: JWT authentication API, user creation, login, password hashing (`passlib`, `bcrypt`).
    - `todos.py`: Todo CRUD API, validation, error handling.
  - `templates/`: HTML templates (Jinja2) for rendering web pages.
  - `static/`: Static files (CSS, JavaScript) served directly by the application.
  - `test/`: Contains integration tests for the endpoints
- `books.py`, `books2.py`: Example APIs for books, with validation, path/query params, CRUD methods, status codes, and error handling.

### Conventions Adopted

* **Dependency Injection** : Database access is managed via dependencies (`db_dependency`) to ensure each request has an isolated DB session.
* **Separation of Concerns** : Logic is separated into routers (API), models (data), and templates (view), following an MVC-like approach.
* **Hybrid Authentication** :
  * **Web Pages** : Authentication is managed via a JWT token saved in a **cookie** (`access_token`).
  * **API** : Authentication expects a **Bearer Token** in the `Authorization` header, as per the OAuth2 standard.
* **Validation** : Pydantic is used to validate incoming data in API requests, ensuring data integrity.
* **Error Handling** : HTTP errors are handled with `HTTPException` and explicit status codes.

## 📚 API and Documentation

Once the server is running, the interactive API documentation (generated by Swagger UI) is available at:

* **Swagger UI** : `http://127.0.0.1:8000/docs`

**All pip install:**

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
pip install pytest
pip install httpx
pip install pytest-asyncio
pip install aiofiles
pip install jinja2
```

## 🗃️ Development Commands & Workflow

### Alembic (Database Migrations)

* alembic init `<folder>` - Initialized a new, generic env
* **Create a new migration** (after changing `models.py`):
  ```
  alembic revision --autogenerate -m "Description of the change"
  ```
* **Apply migrations** :

```
  alembic upgrade head
```

* **Rollback the last migration** :

```
  alembic downgrade -1
```

### Alembic.ini - All configurations

- sqlalchemy.url = driver://user:pass@localhost/dbname

### SQLite Commands

```
# Connect to the database
sqlite3 TodoApp/todosapp.db

# Show table schema
.schema

# Set display mode to table
.mode table

# Run queries
select * from user;
select * from todo;

# Exit
.quit
```

### Kill processes on port 8000 (Windows):

```sh
#Commands to kill a process stuck on port 8000.

# Find the PID using port 8000
netstat -ano | findstr :8000

# Force kill the process by PID
taskkill /PID <PID_FOUND> /F

```

**Useful SQLite commands:**

```sql
# Connect to the database
sqlite3 TodoApp/todosapp.db

# Show table schema
.schema

# Set display mode to table
.mode table

# Run queries
select * from user;
select * from todo;

# Exit
.quit
```

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

* `from fastapi import FastAPI, APIRouter, Depends, HTTPException, Path, Body, Query`
  * **Usage** : Core FastAPI imports for app creation, modular routers, dependency injection, error handling, and parameter validation.
* `from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer`
  * **Usage** : OAuth2 authentication utilities for login and token management.
* `from starlette import status`
  * **Usage** : Constants for HTTP status codes (e.g., `status.HTTP_201_CREATED`).
* `from pydantic import BaseModel, Field`
  * **Usage** : Data validation and serialization (request/response models, field constraints).
* `from typing import Annotated, Optional`
  * **Usage** : Type hints for dependency injection (e.g., `db_dependency = Annotated[...]`).
* `from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine`
  * **Usage** : SQLAlchemy ORM for table/model definitions and DB engine creation.
* `from sqlalchemy.orm import Session, sessionmaker`
  * **Usage** : SQLAlchemy ORM for DB session management.
* `from jose import JWTError, jwt`
  * **Usage** : JWT encoding/decoding for authentication.
* `from passlib.context import CryptContext`
  * **Usage** : Password hashing and verification (e.g., `bcrypt_context`).
