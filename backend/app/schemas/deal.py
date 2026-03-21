"""Deal-related schemas."""

from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class DealResponse(BaseModel):
    id: UUID
    product_id: UUID
    source_platform: str
    buy_price: float
    sell_price: float
    roi_pct: float
    fba_fee: float
    referral_fee: float
    prep_cost: float
    shipping_cost: float
    net_profit: float
    score: int
    score_label: Optional[str]
    status: str
    discovered_at: datetime
    product_title: Optional[str] = None
    product_asin: Optional[str] = None
    product_image_url: Optional[str] = None
    product_category: Optional[str] = None

    class Config:
        from_attributes = True


class DealListResponse(BaseModel):
    items: List[DealResponse]
    total: int
    page: int
    page_size: int


class DealFilter(BaseModel):
    min_roi: Optional[float] = None
    max_roi: Optional[float] = None
    min_score: Optional[int] = None
    categories: Optional[List[str]] = None
    status: Optional[str] = None
    source_platform: Optional[str] = None
    sort_by: str = "score"
    sort_order: str = "desc"


class DealScoreResponse(BaseModel):
    asin: str
    composite_score: int
    score_label: str
    roi_factor: float
    bsr_factor: float
    competition_factor: float
    price_stability_factor: float
    availability_factor: float


class BatchScoreRequest(BaseModel):
    asins: List[str] = Field(..., max_length=50)
