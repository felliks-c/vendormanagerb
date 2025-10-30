from sqlalchemy.orm import Session 
from app.models import Vendor
from app.schemas import Vendor

def get_vendors(db: Session, skip: int = 0, limit: int = 100) -> list[Vendor]:
    """
    Возвращает список всех объектов Vendor с пагинацией.
    """
    return db.query(Vendor).offset(skip).limit(limit).all()