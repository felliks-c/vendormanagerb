from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

# 1. Строка подключения для SQLite (асинхронная)
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

# 2. Создание асинхронного движка
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # можно включить для логирования всех SQL-запросов
    future=True
)

# 3. Создание фабрики сессий
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False
)

# 4. Базовый класс для моделей
Base = declarative_base()

# 5. Dependency для FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session