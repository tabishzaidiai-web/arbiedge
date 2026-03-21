"""User settings and preferences endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional, List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_preferences import UserPreferences
from app.models.user import User

router = APIRouter()


class PreferencesUpdate(BaseModel):
    min_roi_pct: Optional[float] = Field(None, ge=0, le=500)
    max_buy_cost: Optional[float] = Field(None, ge=0)
    preferred_categories: Optional[List[str]] = None
    excluded_brands: Optional[List[str]] = None
    excluded_categories: Optional[List[str]] = None
    prep_cost_default: Optional[float] = Field(None, ge=0)
    inbound_shipping_cost_per_lb: Optional[float] = Field(None, ge=0)
    storage_duration_days: Optional[int] = Field(None, ge=0)
    email_send_time: Optional[str] = None
    min_score_threshold: Optional[int] = Field(None, ge=0, le=100)
    email_digest_enabled: Optional[bool] = None


@router.get("/preferences")
async def get_preferences(user_id: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get user's deal filtering preferences."""
    result = await db.execute(select(UserPreferences).where(UserPreferences.user_id == user_id))
    prefs = result.scalar_one_or_none()
    if not prefs:
        return {"message": "No preferences set", "defaults": {"min_roi_pct": 30, "max_buy_cost": 50, "min_score_threshold": 70}}
    return prefs


@router.post("/preferences")
async def update_preferences(
    data: PreferencesUpdate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create or update user preferences."""
    result = await db.execute(select(UserPreferences).where(UserPreferences.user_id == user_id))
    prefs = result.scalar_one_or_none()
    if not prefs:
        prefs = UserPreferences(user_id=user_id)
        db.add(prefs)
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(prefs, key, value)
    await db.flush()
    await db.refresh(prefs)
    return prefs


@router.put("/settings")
async def update_user_settings(
    full_name: Optional[str] = None,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user profile settings."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if full_name is not None:
        user.full_name = full_name
    await db.flush()
    return {"message": "Settings updated"}
