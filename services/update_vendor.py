from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Vendor
from schemas import VendorUpdate

# ---------- Обновление ----------
async def update_vendor(db: AsyncSession, vendor_data: VendorUpdate) -> Vendor:
    query = await db.execute(select(Vendor).where(Vendor.id == vendor_data.id))
    vendor = query.scalars().first()
    if not vendor:
        raise ValueError(f"Поставщик с id={vendor_data.id} не найден")

    for field, value in vendor_data.dict(exclude={"id"}, exclude_none=True).items():
        setattr(vendor, field, value)

    await db.commit()
    await db.refresh(vendor)
    return vendor