from sqlalchemy.orm import Session
from app.models import Vendor
from app.schemas import Vendor
from typing import Optional


def delete_vendor(db: Session, vendor_id: int) -> Optional[Vendor]:
    """
    Удаляет объект Vendor, найденный по ID.
    """
    # 1. Ищем объект по ID
    db_vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
    
    if db_vendor:
        # 2. Удаляем объект и фиксируем транзакцию
        db.delete(db_vendor)
        db.commit()
        return db_vendor # Возвращаем удаленный объект, чтобы показать, что удаление было успешным
        
    # Если объект не найден
    return None