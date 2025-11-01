from fastapi import FastAPI
import uvicorn
from routers.vendors import router as vendors_router


app = FastAPI(title="Vendor Manager", version="0.1.0")

# Корневой маршрут
@app.get("/")
async def read_root():
    return {"message": "Приложение запущено"}

@app.get("/test")
async def read_root():
    return {"status": "success"}

app.include_router(vendors_router)

if __name__ == "__main__":
    # Запуск для разработки
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)