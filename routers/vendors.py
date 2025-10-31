from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio

# Импорт вашей конфигурации:
#from database import get_db # Предполагаем, что database.py на один уровень выше
from schemas import Vendor, VendorCreate, VendorUpdate, VendorBase
# Импорт функций CRUD из вашего модуля vendors
from services import create_vendor, get_vendors, update_vendor, delete_vendor 
# Также нужен импорт модели, если вы хотите искать по ней, но здесь он не обязателен
# from .. import models 

# Создаем роутер с префиксом и тегами
router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"],
)

# ==============================================================================
# 1. POST /vendors/ (CREATE) - Создание нового поставщика
# ==============================================================================
@router.post("/", response_model=Vendor, status_code=status.HTTP_201_CREATED)
async def create_vendor_endpoint(vendor: VendorCreate):
    """
    Создает нового поставщика в базе данных.
    """
    # Дополнительная проверка, если нужно убедиться, что email уникален
    # existing_vendor = db.query(models.Vendor).filter(models.Vendor.contactEmail == vendor.contactEmail).first()
    # if existing_vendor:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, 
    #         detail="Email already registered"
    #     )

    
        
    return await create_vendor(db=db, vendor=vendor)

# ==============================================================================
# 2. GET /vendors/ (READ ALL) - Получение списка поставщиков
# ==============================================================================
@router.get("/", response_model=List[Vendor])
def read_vendors_endpoint(skip: int = 0, limit: int = 100):
    """
    Возвращает список всех поставщиков с пагинацией.
    """
    return get_vendors(db, skip=skip, limit=limit)

# ==============================================================================
# 3. PUT /vendors/{vendor_id} (UPDATE) - Обновление данных поставщика
# ==============================================================================
@router.put("/{vendor_id}", response_model=Vendor)
def update_vendor_endpoint(vendor_id: int, vendor_data: VendorUpdate):
    """
    Обновляет данные поставщика по его ID.
    """
    # Проверяем, что есть хоть какие-то данные для обновления
    if not vendor_data.dict(exclude_unset=True):
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No fields provided for update"
        )
        
    updated_vendor = update_vendor(db=db, vendor_id=vendor_id, vendor_data=vendor_data)
    
    if updated_vendor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Vendor with id {vendor_id} not found"
        )
        
    return updated_vendor

# ==============================================================================
# 4. DELETE /vendors/{vendor_id} (DELETE) - Удаление поставщика
# ==============================================================================
@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor_endpoint(vendor_id: int):
    """
    Удаляет поставщика по его ID.
    """
    deleted_vendor = delete_vendor(vendor_id)
    
    if deleted_vendor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Vendor with id {vendor_id} not found"
        )
        
    # Возвращаем пустой ответ с кодом 204 (No Content), т.к. объект удален
    return

# ==============================================================================