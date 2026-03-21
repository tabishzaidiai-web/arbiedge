"""Product schemas."""

from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class ProductResponse(BaseModel):
    id: UUID
    asin: str
    title: str
    category: Optional[str]
    brand: Optional[str]
    review_count: Optional[int]
    star_rating: Optional[float]
    bsr_current: Optional[int]
    bsr_30day_avg: Optional[int]
    image_url: Optional[str]
    amazon_url: Optional[str]
    fulfillment_type: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int


class ProductSearch(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    min_bsr: Optional[int] = None
    max_bsr: Optional[int] = None
    min_rating: Optional[float] = None
