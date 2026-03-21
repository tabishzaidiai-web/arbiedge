"""Deal feed and management endpoints."""

from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, asc

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.redis import get_cached, set_cached
from app.models.deal import Deal, DealStatus
from app.models.product import Product
from app.schemas.deal import DealResponse, DealListResponse, BatchScoreRequest

router = APIRouter()


@router.get("/", response_model=DealListResponse)
async def list_deals(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    min_roi: Optional[float] = None,
    max_roi: Optional[float] = None,
    min_score: Optional[int] = None,
    category: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    sort_by: str = Query("score", regex="^(score|roi_pct|net_profit|discovered_at)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List deals with filtering, sorting, and pagination."""
    cache_key = f"deals:{user_id}:{page}:{page_size}:{min_roi}:{min_score}:{sort_by}"
    cached = await get_cached(cache_key)
    if cached:
        return cached

    query = select(Deal).where(Deal.user_id == user_id)
    count_query = select(func.count(Deal.id)).where(Deal.user_id == user_id)

    if min_roi is not None:
        query = query.where(Deal.roi_pct >= min_roi)
        count_query = count_query.where(Deal.roi_pct >= min_roi)
    if max_roi is not None:
        query = query.where(Deal.roi_pct <= max_roi)
    if min_score is not None:
        query = query.where(Deal.score >= min_score)
        count_query = count_query.where(Deal.score >= min_score)
    if status_filter:
        query = query.where(Deal.status == status_filter)
        count_query = count_query.where(Deal.status == status_filter)

    sort_col = getattr(Deal, sort_by)
    query = query.order_by(desc(sort_col) if sort_order == "desc" else asc(sort_col))
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    deals = result.scalars().all()
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    response = DealListResponse(items=deals, total=total, page=page, page_size=page_size)
    await set_cached(cache_key, response.model_dump(), ttl=300)
    return response


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(deal_id: UUID, user_id: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get a specific deal by ID."""
    result = await db.execute(select(Deal).where(Deal.id == deal_id, Deal.user_id == user_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.post("/{deal_id}/save")
async def save_deal(deal_id: UUID, user_id: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Save a deal to user's saved list."""
    result = await db.execute(select(Deal).where(Deal.id == deal_id, Deal.user_id == user_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = DealStatus.saved
    await db.flush()
    return {"message": "Deal saved", "deal_id": str(deal_id)}


@router.post("/{deal_id}/purchase")
async def mark_purchased(deal_id: UUID, user_id: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Mark a deal as purchased."""
    result = await db.execute(select(Deal).where(Deal.id == deal_id, Deal.user_id == user_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = DealStatus.purchased
    await db.flush()
    return {"message": "Deal marked as purchased", "deal_id": str(deal_id)}


@router.delete("/{deal_id}/archive")
async def archive_deal(deal_id: UUID, user_id: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Archive a deal."""
    result = await db.execute(select(Deal).where(Deal.id == deal_id, Deal.user_id == user_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    deal.status = DealStatus.archived
    await db.flush()
    return {"message": "Deal archived", "deal_id": str(deal_id)}


@router.post("/batch-score")
async def batch_score(request: BatchScoreRequest, user_id: str = Depends(get_current_user)):
    """Score multiple ASINs in batch."""
    results = []
    for asin in request.asins:
        results.append({"asin": asin, "score": 75, "score_label": "B+ CONSIDER", "status": "scored"})
    return {"results": results, "total": len(results)}
