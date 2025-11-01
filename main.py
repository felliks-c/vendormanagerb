from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import uvicorn
import os
from routers.vendors import router as vendors_router


app = FastAPI(title="Vendor Manager", version="0.1.0")

# Корневой маршрут
@app.get("/")
async def read_root():
    return {"message": "Приложение запущено"}

@app.get("/test")
async def read_root():
    return {"status": "success"}

def load_private_key():
    key_path = os.getenv("PRIVATE_KEY_PATH", "/run/secrets/vendormanagerb.pem")
    with open(key_path, "r") as f:
        private_key = f.read()
    return private_key


# Подключаем роутер к приложению
app.include_router(vendors_router)


# Пример как подключать роутеры из других модулей:
# from .routes.vendors import router as vendors_router
# app.include_router(vendors_router, prefix="/vendors", tags=["vendors"])


if __name__ == "__main__":
    # Запуск для разработки
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)