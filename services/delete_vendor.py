from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Vendor
from schemas import VendorDelete

# ---------- Удаление ----------
async def delete_vendor(db: AsyncSession, vendor_data: VendorDelete) -> dict:
    query = await db.execute(select(Vendor).where(Vendor.id == vendor_data.id))
    vendor = query.scalars().first()
    if not vendor:
        raise ValueError(f"Поставщик с id={vendor_data.id} не найден")

    await db.delete(vendor)
    await db.commit()
    return {"message": f"Поставщик id={vendor_data.id} удалён"}