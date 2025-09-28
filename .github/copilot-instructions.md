# Copilot Instructions for AI Agents

## Project Overview

This codebase is a FastAPI-based collection of projects, including a Todo application and book-related APIs. It uses a modular structure with separate scripts and a dedicated `TodoApp` package for the main app logic.

## Key Components

-   `TodoApp/`: Main FastAPI app for todo management. Contains:
    -   `main.py`: FastAPI app entrypoint (imported as `main:app` for uvicorn)
    -   `database.py`: SQLite3 database setup and connection
    -   `models.py`: Pydantic models and ORM models
    -   `routers/`: API route modules (`auth.py`, `todos.py`)
    -   `run.py`: Script to launch the app
-   `books.py`, `books2.py`: Standalone FastAPI scripts for book APIs
-   `run_book.py`, `run_book2.py`, `run_TodoApp.py`: Entrypoint scripts for running different apps

## Developer Workflows

-   **Run TodoApp locally:**
    ```sh
    cd ./TodoApp
    uvicorn main:app --reload
    ```
-   **Kill process on port 8000 (Windows):**
    ```sh
    netstat -ano | findstr :8000
    taskkill /PID <PID> /F
    ```
-   **Install form support:**
    ```sh
    pip install python-multipart
    ```

## Project Conventions

-   API routers are organized in `TodoApp/routers/` and included in `main.py`.
-   Database is SQLite3, file at `TodoApp/todosapp.db`.
-   JWT authentication is referenced (see `https://www.jwt.io/`), likely implemented in `auth.py`.
-   Use Pydantic for data validation and SQLAlchemy for ORM.
-   Scripts in the root directory are for running or testing individual modules.

## Integration & Patterns

-   All API endpoints are defined in router modules and registered in `main.py`.
-   Database access is abstracted in `database.py` and used via dependencies.
-   Authentication logic is separated in `routers/auth.py`.

## Examples

-   To add a new API route, create a module in `TodoApp/routers/` and register it in `main.py`.
-   To update models, edit `models.py` and apply changes to the database if needed.

## References

-   See `README.md` for quick commands and JWT info.
-   See `usare_sqlite3.md` for SQLite usage notes.

---

Update this file as project structure or conventions evolve.
