# run.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",          # formato "<file>:<app>"
        host="127.0.0.1",
        port=8000,
        reload=True,         # ricarica automatica in sviluppo
        log_level="info"     # "debug" se vuoi vedere tutti i dettagli
    )
