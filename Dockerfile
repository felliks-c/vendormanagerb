# --- 1. Базовый образ ---
FROM python:3.12-slim

# --- 2. Установка системных пакетов ---
# (build-essential и libpq-dev — для нормальной работы psycopg2 и сборки зависимостей)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --- 3. Настройки окружения ---
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

# --- 4. Рабочая директория ---
WORKDIR /code

# --- 5. Копируем зависимости и устанавливаем их отдельно ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- 6. Копируем весь проект ---
COPY . .

# --- 7. Экспонируем порт ---
EXPOSE 3000

# --- 8. Команда запуска ---
# Так как main.py лежит в корне, путь простой: main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
