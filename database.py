from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Строка подключения
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. Создание движка (Engine)
# 'connect_args={"check_same_thread": False}' нужен только для SQLite, 
# чтобы позволить нескольким потокам обрабатывать запросы. 
# SQLite по умолчанию разрешает только одному потоку взаимодействовать.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Создание фабрики сессий (SessionLocal)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Базовый класс для моделей (Base)
Base = declarative_base()

# В вашем FastAPI роутере или зависимостях (dependencies) вы будете использовать 
# SessionLocal для создания сессий, например, так:
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()