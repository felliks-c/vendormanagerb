# Vendor Manager API

## Описание проекта

Vendor Manager - это REST API приложение для управления поставщиками, построенное на FastAPI с использованием SQLAlchemy и SQLite. Система предоставляет полный CRUD функционал для работы с базой данных поставщиков.

## Технологический стек

- **Framework:** FastAPI
- **База данных:** SQLite с асинхронным драйвером (aiosqlite)
- **ORM:** SQLAlchemy 2.0 (async)
- **Валидация:** Pydantic
- **Сервер:** Uvicorn
- **Контейнеризация:** Docker + Docker Compose
- **CI/CD:** GitHub Actions + Watchtower (автоматическое обновление)

## Структура проекта

```
vendormanagerb/
├── main.py                # Точка входа приложения
├── database.py            # Конфигурация базы данных
├── models.py              # SQLAlchemy модели
├── schemas.py             # Pydantic схемы валидации
├── routers/
│   └── vendors.py         # API эндпоинты для поставщиков
├── services/              # Бизнес-логика
│   ├── create_vendor.py   # Создание поставщика
│   ├── update_vendor.py   # Обновление поставщика
│   ├── delete_vendor.py   # Удаление поставщика
│   └── get_vendors.py     # Получение и поиск поставщиков
├── middleware/            # Middleware компоненты
├── docker-compose.yml     # Docker Compose конфигурация
├── Dockerfile            # Docker образ
└── requirements.txt      # Python зависимости
```

## Установка и запуск

### Локальный запуск

1. Клонировать репозиторий:
```bash
git clone <repository-url>
cd vendormanagerb
```

2. Создать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Создать файл `.env` (опционально, см. `.env.example`)

5. Запустить приложение:
```bash
python main.py
```

Приложение будет доступно по адресу: `http://127.0.0.1:8000`

### Запуск через Docker

1. Запустить с помощью Docker Compose:
```bash
docker-compose up -d
```

Приложение будет доступно по адресу: `http://localhost:3000`

## API Документация

После запуска приложения доступна интерактивная документация:
- **Swagger UI:** `http://localhost:8000/docs` (или порт 3000 для Docker)
- **ReDoc:** `http://localhost:8000/redoc`

## Модель данных

### Vendor (Поставщик)

| Поле         | Тип     | Описание                          | Ограничения          |
|--------------|---------|-----------------------------------|---------------------|
| id           | Integer | Уникальный идентификатор          | Primary Key         |
| name         | String  | Имя поставщика                    | Required            |
| contactEmail | String  | Контактный email                  | Required, Unique    |
| category     | String  | Категория (Tech, Food, Services) | Required            |
| rating       | Float   | Рейтинг поставщика               | 0.0 - 5.0           |

## API Эндпоинты

### 1. Создание поставщика

**POST** `/vendors/`

Создаёт нового поставщика в системе.

**Request Body:**
```json
{
  "name": "Tech Supplies Inc.",
  "contactEmail": "contact@techsupplies.com",
  "category": "Tech",
  "rating": 4.5
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Tech Supplies Inc.",
  "contactEmail": "contact@techsupplies.com",
  "category": "Tech",
  "rating": 4.5
}
```

**Ошибки:**
- `400 Bad Request` - если email уже существует или данные некорректные

### 2. Обновление поставщика

**PUT** `/vendors/`

Обновляет существующего поставщика. ID обязателен, остальные поля опциональны.

**Request Body:**
```json
{
  "id": 1,
  "name": "Updated Tech Supplies",
  "rating": 4.8
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Updated Tech Supplies",
  "contactEmail": "contact@techsupplies.com",
  "category": "Tech",
  "rating": 4.8
}
```

**Ошибки:**
- `404 Not Found` - если поставщик с указанным ID не найден

### 3. Удаление поставщика

**DELETE** `/vendors/`

Удаляет поставщика по ID.

**Request Body:**
```json
{
  "id": 1
}
```

**Response:** `200 OK`
```json
{
  "message": "Поставщик id=1 удалён"
}
```

**Ошибки:**
- `404 Not Found` - если поставщик с указанным ID не найден

### 4. Получение списка поставщиков

**GET** `/vendors/`

Получает список поставщиков с возможностью фильтрации и пагинации.

**Query Parameters:**
- `id` (int) - фильтр по ID
- `name` (string) - фильтр по имени
- `contactEmail` (string) - фильтр по email
- `category` (string) - фильтр по категории
- `rating` (float) - фильтр по рейтингу
- `limit` (int) - количество записей (по умолчанию: 100)
- `offset` (int) - смещение для пагинации (по умолчанию: 0)

**Пример запроса:**
```
GET /vendors/?category=Tech&limit=50&offset=0
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Tech Supplies Inc.",
    "contactEmail": "contact@techsupplies.com",
    "category": "Tech",
    "rating": 4.5
  }
]
```

### 5. Поиск поставщиков

**GET** `/vendors/search`

Поиск по частичным совпадениям. Возвращает максимум 10 результатов.

**Query Parameters:**
- `id` (string) - поиск по подстроке в ID
- `name` (string) - поиск по подстроке в имени
- `contactEmail` (string) - поиск по подстроке в email
- `category` (string) - поиск по подстроке в категории
- `rating` (string) - поиск по подстроке в рейтинге

**Пример запроса:**
```
GET /vendors/search?name=Tech&category=Inc
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Tech Supplies Inc.",
    "contactEmail": "contact@techsupplies.com",
    "category": "Tech",
    "rating": 4.5
  }
]
```

**Примечание:** При указании нескольких параметров применяется логика AND (все условия должны совпадать).

## Особенности реализации

### Асинхронная архитектура
- Все операции с базой данных выполняются асинхронно
- Используется `AsyncSession` для работы с SQLAlchemy
- Применяется `aiosqlite` для асинхронного взаимодействия с SQLite

### Валидация данных
- Pydantic схемы для валидации входящих и исходящих данных
- EmailStr для валидации email адресов
- Ограничения на рейтинг (0.0 - 5.0)

### Lazy Loading и пагинация
- Поддержка `limit` и `offset` для постраничной загрузки
- Оптимизированные запросы к базе данных

### Автоматическое развертывание
- GitHub Actions для CI/CD
- Автоматическая сборка и публикация Docker образа
- Watchtower для автоматического обновления контейнеров

## Переменные окружения

Создайте файл `.env` в корне проекта (см. `.env.example`):

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./sql_app.db

# Server
HOST=127.0.0.1
PORT=8000
```

## Требования

- Python 3.12+
- SQLite 3
- Docker и Docker Compose (для контейнеризации)

## Основные зависимости

- `fastapi==0.120.1` - веб-фреймворк
- `uvicorn==0.38.0` - ASGI сервер
- `sqlalchemy==2.0.44` - ORM
- `aiosqlite==0.21.0` - асинхронный драйвер SQLite
- `pydantic==2.12.3` - валидация данных
- `email-validator==2.3.0` - валидация email

## Разработка

### Запуск в режиме разработки

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Тестирование

```bash
pytest
```

## Лицензия

[Укажите вашу лицензию]

## Контакты

[Ваши контактные данные]