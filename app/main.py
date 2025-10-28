from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import uvicorn
from routers.vendors import create_item, list_items

# app/main.py
# Базовая структура FastAPI-приложения, куда можно добавлять маршруты (роуты).


app = FastAPI(title="Vendor Manager", version="0.1.0")

# Корневой маршрут
@app.get("/")
async def read_root():
    return {"message": "Приложение запущено"}


# Пример отдельного роутера для группировки эндпоинтов (например /api)
api_router = APIRouter(prefix="/api", tags=["api"])


class Item(BaseModel):
    id: int
    name: str





# Подключаем роутер к приложению
app.include_router(api_router)


# Пример как подключать роутеры из других модулей:
# from .routes.vendors import router as vendors_router
# app.include_router(vendors_router, prefix="/vendors", tags=["vendors"])


if __name__ == "__main__":
    # Запуск для разработки
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)