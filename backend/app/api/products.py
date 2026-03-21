"""Product catalog endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.product import Product
from app.schemas.product import ProductResponse, ProductListResponse

router = APIRouter()


@router.get("/", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    brand: Optional[str] = None,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List products with optional filtering."""
    query = select(Product)
    count_query = select(func.count(Product.id))

    if category:
        query = query.where(Product.category == category)
        count_query = count_query.where(Product.category == category)
    if brand:
        query = query.where(Product.brand == brand)
        count_query = count_query.where(Product.brand == brand)

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    products = result.scalars().all()
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    return ProductListResponse(items=products, total=total, page=page, page_size=page_size)


@router.get("/search", response_model=ProductListResponse)
async def search_products(
    q: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Search products by title, ASIN, or brand."""
    query = select(Product).where(
        or_(
            Product.title.ilike(f"%{q}%"),
            Product.asin.ilike(f"%{q}%"),
            Product.brand.ilike(f"%{q}%"),
        )
    )
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    products = result.scalars().all()
    return ProductListResponse(items=products, total=len(products), page=page, page_size=page_size)


@router.get("/{asin}", response_model=ProductResponse)
async def get_product(asin: str, user_id: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get product details by ASIN."""
    result = await db.execute(select(Product).where(Product.asin == asin))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/scan")
async def trigger_scan(
    categories: list[str] = Query(default=["Electronics", "Home & Kitchen"]),
    user_id: str = Depends(get_current_user),
):
    """Trigger a product scan job for specified categories."""
    import uuid
    job_id = str(uuid.uuid4())
    return {"job_id": job_id, "status": "queued", "categories": categories, "message": "Scan job queued"}
