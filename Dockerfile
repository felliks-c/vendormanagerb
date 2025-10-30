# --- 1. Базовый образ ---
FROM python:3.12-slim

# --- 2. Установка системных пакетов (если нужно что-то вроде psycopg2) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --- 3. Настройки окружения ---
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=3000
WORKDIR /code

COPY . /code

# --- 4. Установка зависимостей ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/code

# --- 5. Копируем весь проект ---
# COPY . .

# --- 6. Экспонируем порт ---
EXPOSE 3000

# --- 7. Запуск через uvicorn --
CMD ["uvicorn", "m", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
