from pydantic import BaseModel, EmailStr
from typing import Optional

# Базовая схема для общих полей
class VendorBase(BaseModel):
    name: str
    contactEmail: EmailStr
    category: str
    rating: float = 0.0

# Схема для создания (наследует базу)
class VendorCreate(VendorBase):
    pass

# Схема для обновления (все поля опциональны, кроме обязательных)
class VendorUpdate(BaseModel):
    name: Optional[str] = None
    contactEmail: Optional[EmailStr] = None
    category: Optional[str] = None
    rating: Optional[float] = None
    
# Схема для чтения (включает id)
class Vendor(VendorBase):
    id: int

    class Config:
        orm_mode = True # Позволяет Pydantic работать с ORM-объектами SQLAlchemy