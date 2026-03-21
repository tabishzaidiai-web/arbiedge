"""User preferences for deal filtering and notifications."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, Integer, Boolean, DateTime, ForeignKey, func, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    min_roi_pct: Mapped[float] = mapped_column(Float, nullable=False, default=30.0)
    max_buy_cost: Mapped[float] = mapped_column(Float, nullable=False, default=50.0)
    preferred_categories: Mapped[Optional[list]] = mapped_column(ARRAY(String), nullable=True)
    excluded_brands: Mapped[Optional[list]] = mapped_column(ARRAY(String), nullable=True)
    excluded_categories: Mapped[Optional[list]] = mapped_column(ARRAY(String), nullable=True)
    prep_cost_default: Mapped[float] = mapped_column(Float, nullable=False, default=0.50)
    inbound_shipping_cost_per_lb: Mapped[float] = mapped_column(Float, nullable=False, default=0.40)
    storage_duration_days: Mapped[int] = mapped_column(Integer, nullable=False, default=90)
    email_send_time: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, default="07:00")
    min_score_threshold: Mapped[int] = mapped_column(Integer, nullable=False, default=70)
    email_digest_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="preferences")
