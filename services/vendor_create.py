from sqlalchemy.orm import Session
from models import Vendor
from schemas import VendorCreate

def create_vendor(db: Session, vendor: VendorCreate) -> Vendor:
    """
    Создает и сохраняет новый объект Vendor в базе данных.
    """
    # Создаем экземпляр модели Vendor из данных Pydantic схемы
    db_vendor = Vendor(
        name=vendor.name,
        contactEmail=vendor.contactEmail,
        category=vendor.category,
        rating=vendor.rating
    )
    
    # Добавляем объект в сессию, фиксируем транзакцию и обновляем объект
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor