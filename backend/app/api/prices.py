"""Price cross-referencing and snapshot endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.redis import get_cached, set_cached
from app.models.price_snapshot import PriceSnapshot
from app.models.product import Product

router = APIRouter()


@router.get("/cross-reference/{asin}")
async def cross_reference_prices(
    asin: str,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get cross-referenced prices from multiple retailers for an ASIN."""
    cache_key = f"xref:{asin}"
    cached = await get_cached(cache_key)
    if cached:
        return cached

    result = await db.execute(select(Product).where(Product.asin == asin))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    snap_result = await db.execute(
        select(PriceSnapshot)
        .where(PriceSnapshot.product_id == product.id)
        .order_by(desc(PriceSnapshot.captured_at))
        .limit(20)
    )
    snapshots = snap_result.scalars().all()

    prices = {}
    for snap in snapshots:
        if snap.source_platform not in prices:
            prices[snap.source_platform] = {
                "platform": snap.source_platform,
                "price": snap.price,
                "availability": snap.availability_status,
                "source_url": snap.source_url,
                "captured_at": str(snap.captured_at),
            }

    response = {"asin": asin, "title": product.title, "prices": list(prices.values())}
    await set_cached(cache_key, response, ttl=1800)
    return response


@router.get("/snapshot/{asin}")
async def price_history(
    asin: str,
    limit: int = 30,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get price history snapshots for an ASIN."""
    result = await db.execute(select(Product).where(Product.asin == asin))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    snap_result = await db.execute(
        select(PriceSnapshot)
        .where(PriceSnapshot.product_id == product.id)
        .order_by(desc(PriceSnapshot.captured_at))
        .limit(limit)
    )
    snapshots = snap_result.scalars().all()

    return {
        "asin": asin,
        "title": product.title,
        "snapshots": [
            {
                "platform": s.source_platform,
                "price": s.price,
                "availability": s.availability_status,
                "captured_at": str(s.captured_at),
            }
            for s in snapshots
        ],
    }
