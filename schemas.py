from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# ---------- Базовая схема ----------
class VendorBase(BaseModel):
    name: str = Field(..., example="Tech Supplies Inc.")
    contactEmail: EmailStr = Field(..., example="contact@techsupplies.com")
    category: str = Field(..., example="Tech")
    rating: float = Field(..., ge=0, le=5, example=4.3)


# ---------- Создание ----------
class VendorCreate(VendorBase):
    """Схема для создания нового поставщика (все поля обязательны)."""
    pass


# ---------- Обновление ----------
class VendorUpdate(BaseModel):
    """Схема для обновления поставщика — id обязателен, остальные поля опциональны."""
    id: int
    name: Optional[str] = Field(None, example="Updated Name")
    contactEmail: Optional[EmailStr] = Field(None, example="newemail@vendor.com")
    category: Optional[str] = Field(None, example="Food")
    rating: Optional[float] = Field(None, ge=0, le=5, example=4.8)


# ---------- Удаление ----------
class VendorDelete(BaseModel):
    """Схема для удаления поставщика (нужно указать id)."""
    id: int


# ---------- Получение ----------
class VendorGet(BaseModel):
    """Схема для запроса поставщиков — можно указать одно или несколько полей."""
    id: Optional[int] = None
    name: Optional[str] = None
    contactEmail: Optional[EmailStr] = None
    category: Optional[str] = None
    rating: Optional[float] = None


# ---------- Ответ клиенту ----------
class VendorResponse(VendorBase):
    """Схема для отображения данных поставщика в ответе."""
    id: int

    class Config:
        orm_mode = True  # Позволяет напрямую использовать ORM-модель (SQLAlchemy)
