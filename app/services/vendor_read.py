from sqlalchemy.orm import Session 
from models import Vendor
from schemas import Vendor

def get_vendors(db: Session, skip: int = 0, limit: int = 100) -> list[models.Vendor]:
    """
    Возвращает список всех объектов Vendor с пагинацией.
    """
    return db.query(models.Vendor).offset(skip).limit(limit).all()