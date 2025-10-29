from sqlalchemy.orm import Session
from models import Vendor
from schemas import VendorUpdate

def update_vendor(db: Session, vendor_id: int, vendor_data: schemas.VendorUpdate) -> Optional[models.Vendor]:
    """
    Ищет объект Vendor по ID и обновляет его поля на основе полученных данных.
    """
    # 1. Ищем объект по ID
    db_vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    
    if db_vendor:
        # 2. Перебираем поля из Pydantic схемы обновления
        update_data = vendor_data.dict(exclude_unset=True) # Исключаем поля, которые не были переданы
        
        # 3. Обновляем атрибуты модели
        for key, value in update_data.items():
            setattr(db_vendor, key, value)
            
        # 4. Фиксируем изменения
        db.add(db_vendor)
        db.commit()
        db.refresh(db_vendor)
        return db_vendor
    
    # Если объект не найден
    return None