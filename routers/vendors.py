from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any, List

from services import (
    create_vendor,
    update_vendor,
    delete_vendor,
    get_vendors,
    search_vendors
)
from schemas import (
    VendorCreate,
    VendorUpdate,
    VendorDelete,
    VendorResponse
)
from database import get_db

# ---------- Router ----------
router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"],
)

# ---------- Создание ----------
@router.post("/", response_model=VendorResponse)
async def create_vendor_route(vendor: VendorCreate, db: AsyncSession = Depends(get_db)):
    try:
        new_vendor = await create_vendor(db, vendor)
        return new_vendor
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------- Обновление ----------
@router.put("/", response_model=VendorResponse)
async def update_vendor_route(vendor: VendorUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_vendor = await update_vendor(db, vendor)
        return updated_vendor
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ---------- Удаление ----------
@router.delete("/", response_model=Dict[str, str])
async def delete_vendor_route(vendor: VendorDelete, db: AsyncSession = Depends(get_db)):
    try:
        result = await delete_vendor(db, vendor)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ---------- Получение с фильтрацией ----------
@router.get("/", response_model=List[VendorResponse])
async def get_vendors_route(
    name: Optional[str] = None,
    contactEmail: Optional[str] = None,
    category: Optional[str] = None,
    rating: Optional[float] = None,
    id: Optional[int] = None,
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    filters: Dict[str, Any] = {}
    if id is not None:
        filters["id"] = id
    if name:
        filters["name"] = name
    if contactEmail:
        filters["contactEmail"] = contactEmail
    if category:
        filters["category"] = category
    if rating is not None:
        filters["rating"] = rating

    vendors = await get_vendors(db, filters=filters, limit=limit, offset=offset)
    return vendors

# ---------- Топ-10 поиск по частичным совпадениям ----------
@router.get("/search", response_model=List[VendorResponse])
async def search_vendors_route(
    name: Optional[str] = None,
    contactEmail: Optional[str] = None,
    category: Optional[str] = None,
    rating: Optional[str] = None,  # даже числа можно искать как строку
    id: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    search_terms: Dict[str, str] = {}
    if id:
        search_terms["id"] = id
    if name:
        search_terms["name"] = name
    if contactEmail:
        search_terms["contactEmail"] = contactEmail
    if category:
        search_terms["category"] = category
    if rating:
        search_terms["rating"] = rating

    vendors = await search_vendors(db, search_terms=search_terms)
    return vendors
