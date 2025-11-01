from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models import Vendor
from schemas import VendorCreate

# ---------- Создание ----------
async def create_vendor(db: AsyncSession, vendor_data: VendorCreate) -> Vendor:
    new_vendor = Vendor(**vendor_data.dict())
    db.add(new_vendor)
    try:
        await db.commit()
        await db.refresh(new_vendor)  # чтобы получить id и все поля
        return new_vendor
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"Ошибка при создании поставщика: {e.orig}")