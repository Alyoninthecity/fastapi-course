# --- STAGE 1: Il "Costruttore" ---
FROM python:3.11-slim as builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip wheel

# Copia requirements.txt dalla cartella principale (visto che il context è '.')
COPY requirements.txt .

RUN pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt


# --- STAGE 2: L'Immagine "Finale" ---
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*

# --- MODIFICA CHIAVE ---
# Copia il contenuto di ./TodoApp in una NUOVA cartella /app/TodoApp
# Per il PKG che devo fare
COPY ./TodoApp ./TodoApp

EXPOSE 8000

# --- COMANDO DI DEFAULT AGGIORNATO ---
CMD ["uvicorn", "TodoApp.main:app", "--host", "0.0.0.0", "--port", "8000"]