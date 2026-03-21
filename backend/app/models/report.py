"""Report model for daily deal digests."""

import uuid
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey, func, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DeliveryStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    report_type: Mapped[str] = mapped_column(String(50), nullable=False, default="daily_digest")
    deal_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    delivery_status: Mapped[DeliveryStatus] = mapped_column(
        SAEnum(DeliveryStatus), default=DeliveryStatus.pending, nullable=False
    )
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="reports")
