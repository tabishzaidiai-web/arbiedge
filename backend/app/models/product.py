"""Product model representing Amazon ASINs."""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, Integer, DateTime, func, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        Index("ix_products_asin", "asin"),
        Index("ix_products_category", "category"),
        Index("ix_products_brand", "brand"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asin: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    upc: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    brand: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    review_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    star_rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    fulfillment_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, default="FBA")
    bsr_current: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bsr_30day_avg: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    amazon_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    weight_lbs: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    length_in: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    width_in: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    height_in: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    price_snapshots = relationship("PriceSnapshot", back_populates="product", lazy="selectin")
    deals = relationship("Deal", back_populates="product", lazy="selectin")
