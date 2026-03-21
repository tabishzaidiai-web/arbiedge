"""Profit calculator and FBA fee endpoints."""

from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.schemas.profit import ProfitCalculationRequest, ProfitCalculationResponse, FBAFeeBreakdown

router = APIRouter()

# FBA referral fee percentages by category
REFERRAL_FEES = {
    "Electronics": 0.08, "Computers": 0.08, "Camera": 0.08,
    "Home & Kitchen": 0.15, "Kitchen": 0.15, "Toys & Games": 0.15,
    "Sports & Outdoors": 0.15, "Health & Beauty": 0.15, "Grocery": 0.15,
    "Books": 0.15, "Clothing": 0.17, "Shoes": 0.15,
    "Jewelry": 0.20, "Automotive": 0.12, "General": 0.15,
}

# FBA fulfillment fees by size tier (simplified)
def get_fulfillment_fee(weight_lbs: float, length: float, width: float, height: float) -> tuple[float, str]:
    """Calculate FBA fulfillment fee based on dimensions and weight."""
    girth = 2 * (width + height) + length
    
    if length <= 15 and width <= 12 and height <= 0.75 and weight_lbs <= 0.375:
        return 3.22, "Small Standard"
    elif length <= 18 and width <= 14 and height <= 8 and weight_lbs <= 20:
        if weight_lbs <= 0.5:
            return 3.86, "Large Standard"
        elif weight_lbs <= 1:
            return 4.75, "Large Standard"
        elif weight_lbs <= 2:
            return 5.40, "Large Standard"
        else:
            return 5.40 + 0.40 * (weight_lbs - 2), "Large Standard"
    else:
        base = 9.73
        if weight_lbs > 1:
            base += 0.42 * (weight_lbs - 1)
        return base, "Oversize"


@router.post("/calculate", response_model=ProfitCalculationResponse)
async def calculate_profit(req: ProfitCalculationRequest, user_id: str = Depends(get_current_user)):
    """Calculate net profit, ROI, and fee breakdown for a potential deal."""
    referral_pct = REFERRAL_FEES.get(req.category, 0.15)
    referral_fee = round(req.sell_price * referral_pct, 2)
    fulfillment_fee, size_tier = get_fulfillment_fee(req.weight_lbs, req.length_in, req.width_in, req.height_in)
    fulfillment_fee = round(fulfillment_fee, 2)
    storage_fee = round(0.87 * (req.length_in * req.width_in * req.height_in / 1728) * req.storage_months, 2)
    shipping_cost = round(req.weight_lbs * req.shipping_cost_per_lb, 2)

    total_costs = round(req.buy_price + referral_fee + fulfillment_fee + storage_fee + req.prep_cost + shipping_cost, 2)
    net_profit = round(req.sell_price - total_costs, 2)
    roi_pct = round((net_profit / req.buy_price) * 100, 2) if req.buy_price > 0 else 0
    margin_pct = round((net_profit / req.sell_price) * 100, 2) if req.sell_price > 0 else 0
    breakeven = round(total_costs - req.buy_price + req.buy_price, 2)

    return ProfitCalculationResponse(
        buy_price=req.buy_price, sell_price=req.sell_price,
        referral_fee=referral_fee, fulfillment_fee=fulfillment_fee,
        storage_fee=storage_fee, prep_cost=req.prep_cost,
        shipping_cost=shipping_cost, total_costs=total_costs,
        net_profit=net_profit, roi_pct=roi_pct, margin_pct=margin_pct,
        breakeven_price=breakeven, size_tier=size_tier,
        fee_breakdown=FBAFeeBreakdown(
            referral_fee=referral_fee, referral_fee_pct=referral_pct * 100,
            fulfillment_fee=fulfillment_fee,
            storage_fee_monthly=round(storage_fee / max(req.storage_months, 1), 2),
            total_fba_fees=round(referral_fee + fulfillment_fee + storage_fee, 2),
        ),
    )


@router.get("/fba-fees/{asin}")
async def get_fba_fees(asin: str, user_id: str = Depends(get_current_user)):
    """Get estimated FBA fees for a specific ASIN."""
    return {
        "asin": asin,
        "estimated_referral_fee": 4.50,
        "estimated_fulfillment_fee": 5.40,
        "estimated_storage_fee_monthly": 0.45,
        "size_tier": "Large Standard",
        "note": "Connect SP-API for exact fee calculations",
    }
