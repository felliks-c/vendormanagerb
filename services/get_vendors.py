from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from models import Vendor
from typing import Optional, List, Dict, Any

# ---------- Универсальный get с фильтрацией ----------
async def get_vendors(
    db: AsyncSession,
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Vendor]:
    """
    Получение поставщиков с фильтрацией по любым полям.
    - filters: словарь вида {'name': 'Tech', 'category': 'Food'}
    - limit / offset: для lazy loading
    """
    query = select(Vendor)

    if filters:
        for field, value in filters.items():
            if hasattr(Vendor, field) and value is not None:
                query = query.where(getattr(Vendor, field) == value)

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


# ---------- Топ-10 совпадений по частичным значениям ----------
async def search_vendors(
    db: AsyncSession,
    search_terms: Dict[str, str]
) -> List[Vendor]:
    """
    Поиск топ-10 поставщиков, где в указанных полях встречается подстрока.
    - search_terms: словарь вида {'name': 'a', 'category': 'Tech'}
    - Совпадение по всем указанным полям одновременно (AND между полями)
    """
    query = select(Vendor)
    conditions = []

    for field, substring in search_terms.items():
        if hasattr(Vendor, field) and substring:
            conditions.append(getattr(Vendor, field).like(f"%{substring}%"))

    if conditions:
        query = query.where(and_(*conditions))

    query = query.limit(10)
    result = await db.execute(query)
    return result.scalars().all()