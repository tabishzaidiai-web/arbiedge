"""Dashboard KPI and summary endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta, timezone

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.deal import Deal, DealStatus

router = APIRouter()


@router.get("/kpis")
async def get_kpis(user_id: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get dashboard KPI metrics."""
    total_result = await db.execute(select(func.count(Deal.id)).where(Deal.user_id == user_id))
    total_deals = total_result.scalar() or 0

    avg_roi_result = await db.execute(select(func.avg(Deal.roi_pct)).where(Deal.user_id == user_id))
    avg_roi = round(avg_roi_result.scalar() or 0, 1)

    saved_result = await db.execute(
        select(func.count(Deal.id)).where(Deal.user_id == user_id, Deal.status == DealStatus.saved)
    )
    total_saved = saved_result.scalar() or 0

    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    weekly_result = await db.execute(
        select(func.count(Deal.id)).where(Deal.user_id == user_id, Deal.discovered_at >= week_ago)
    )
    deals_this_week = weekly_result.scalar() or 0

    total_profit_result = await db.execute(
        select(func.sum(Deal.net_profit)).where(Deal.user_id == user_id, Deal.status == DealStatus.purchased)
    )
    total_profit = round(total_profit_result.scalar() or 0, 2)

    return {
        "total_deals": total_deals,
        "avg_roi": avg_roi,
        "total_saved": total_saved,
        "deals_this_week": deals_this_week,
        "total_profit": total_profit,
    }


@router.get("/deals")
async def get_top_deals(
    limit: int = Query(10, ge=1, le=50),
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get top-scored deals for the dashboard widget."""
    result = await db.execute(
        select(Deal)
        .where(Deal.user_id == user_id, Deal.status == DealStatus.active)
        .order_by(Deal.score.desc())
        .limit(limit)
    )
    deals = result.scalars().all()
    return {"deals": deals, "total": len(deals)}
