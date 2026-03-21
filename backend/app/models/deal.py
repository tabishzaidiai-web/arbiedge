"""Deal and DealScoreBreakdown models."""

import uuid
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, func, Index, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DealStatus(str, enum.Enum):
    active = "active"
    saved = "saved"
    purchased = "purchased"
    archived = "archived"
    expired = "expired"


class Deal(Base):
    __tablename__ = "deals"
    __table_args__ = (
        Index("ix_deals_user_status", "user_id", "status"),
        Index("ix_deals_score", "score"),
        Index("ix_deals_roi", "roi_pct"),
        Index("ix_deals_discovered", "discovered_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    source_platform: Mapped[str] = mapped_column(String(50), nullable=False, default="walmart")
    buy_price: Mapped[float] = mapped_column(Float, nullable=False)
    sell_price: Mapped[float] = mapped_column(Float, nullable=False)
    roi_pct: Mapped[float] = mapped_column(Float, nullable=False)
    fba_fee: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    referral_fee: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    prep_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.50)
    shipping_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    net_profit: Mapped[float] = mapped_column(Float, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    score_label: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    status: Mapped[DealStatus] = mapped_column(SAEnum(DealStatus), default=DealStatus.active, nullable=False)
    discovered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="deals", lazy="selectin")
    user = relationship("User", back_populates="deals", lazy="selectin")
    score_breakdown = relationship("DealScoreBreakdown", back_populates="deal", uselist=False, lazy="selectin")


class DealScoreBreakdown(Base):
    __tablename__ = "deal_score_breakdowns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("deals.id"), nullable=False, unique=True)
    roi_factor: Mapped[float] = mapped_column(Float, nullable=False)
    bsr_factor: Mapped[float] = mapped_column(Float, nullable=False)
    competition_factor: Mapped[float] = mapped_column(Float, nullable=False)
    price_stability_factor: Mapped[float] = mapped_column(Float, nullable=False)
    availability_factor: Mapped[float] = mapped_column(Float, nullable=False)
    composite_score: Mapped[float] = mapped_column(Float, nullable=False)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    deal = relationship("Deal", back_populates="score_breakdown")
