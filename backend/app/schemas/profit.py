"""Profit calculator schemas."""

from pydantic import BaseModel, Field


class ProfitCalculationRequest(BaseModel):
    buy_price: float = Field(..., gt=0, description="Purchase price from source retailer")
    sell_price: float = Field(..., gt=0, description="Expected Amazon selling price")
    weight_lbs: float = Field(1.0, gt=0, description="Product weight in pounds")
    length_in: float = Field(10.0, gt=0)
    width_in: float = Field(8.0, gt=0)
    height_in: float = Field(4.0, gt=0)
    category: str = Field("General", description="Amazon product category")
    prep_cost: float = Field(0.50, ge=0)
    shipping_cost_per_lb: float = Field(0.40, ge=0)
    storage_months: int = Field(3, ge=0)


class FBAFeeBreakdown(BaseModel):
    referral_fee: float
    referral_fee_pct: float
    fulfillment_fee: float
    storage_fee_monthly: float
    total_fba_fees: float


class ProfitCalculationResponse(BaseModel):
    buy_price: float
    sell_price: float
    referral_fee: float
    fulfillment_fee: float
    storage_fee: float
    prep_cost: float
    shipping_cost: float
    total_costs: float
    net_profit: float
    roi_pct: float
    margin_pct: float
    breakeven_price: float
    size_tier: str
    fee_breakdown: FBAFeeBreakdown
