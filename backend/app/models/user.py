"""User model for ArbiEdge platform."""

import uuid
import enum
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Boolean, DateTime, Enum as SAEnum, func, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SubscriptionTier(str, enum.Enum):
    free = "free"
    starter = "starter"
    pro = "pro"
    enterprise = "enterprise"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    clerk_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, unique=True, index=True)
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    subscription_tier: Mapped[SubscriptionTier] = mapped_column(
        SAEnum(SubscriptionTier), default=SubscriptionTier.free, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    deals = relationship("Deal", back_populates="user", lazy="selectin")
    reports = relationship("Report", back_populates="user", lazy="selectin")
    preferences = relationship("UserPreferences", back_populates="user", uselist=False, lazy="selectin")
