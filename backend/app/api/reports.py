"""Report generation and history endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.report import Report
from app.models.deal import Deal, DealStatus

router = APIRouter()


@router.get("/daily")
async def get_daily_report(user_id: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get today's daily deal report."""
    today = datetime.now(timezone.utc).date()
    result = await db.execute(
        select(Deal)
        .where(Deal.user_id == user_id, Deal.status == DealStatus.active)
        .order_by(Deal.score.desc())
        .limit(25)
    )
    deals = result.scalars().all()
    return {"date": str(today), "deals": deals, "deal_count": len(deals)}


@router.post("/generate")
async def generate_report(user_id: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Generate a custom deal report."""
    count_result = await db.execute(
        select(func.count(Deal.id)).where(Deal.user_id == user_id, Deal.status == DealStatus.active)
    )
    deal_count = count_result.scalar() or 0
    report = Report(user_id=user_id, report_type="custom", deal_count=deal_count)
    db.add(report)
    await db.flush()
    await db.refresh(report)
    return {"report_id": str(report.id), "deal_count": deal_count, "status": "generated"}


@router.get("/history")
async def report_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get historical reports with pagination."""
    result = await db.execute(
        select(Report)
        .where(Report.user_id == user_id)
        .order_by(desc(Report.generated_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    reports = result.scalars().all()
    return {"reports": reports, "page": page, "page_size": page_size}
