"""Common Pydantic schemas used across the API."""

from typing import Any, List
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str
    status_code: int = 400


class SuccessResponse(BaseModel):
    message: str
    success: bool = True


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
