"""Deal scoring engine - calculates composite deal scores."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ScoreBreakdown:
    roi_factor: float
    bsr_factor: float
    competition_factor: float
    price_stability_factor: float
    availability_factor: float
    composite_score: int
    score_label: str


class DealScorer:
    """Scores deals on a 0-100 scale based on multiple weighted factors."""

    WEIGHTS = {
        "roi": 0.30,
        "bsr": 0.25,
        "competition": 0.15,
        "price_stability": 0.15,
        "availability": 0.15,
    }

    LABELS = {
        (90, 101): "A+ STRONG BUY",
        (80, 90): "A BUY",
        (70, 80): "B+ CONSIDER",
        (60, 70): "B MARGINAL",
        (0, 60): "C PASS",
    }

    def score_deal(
        self,
        roi_pct: float,
        bsr_rank: int,
        bsr_category_max: int = 100000,
        num_fba_sellers: int = 5,
        price_volatility_30d: float = 0.05,
        in_stock: bool = True,
        buy_box_stable: bool = True,
    ) -> ScoreBreakdown:
        roi_factor = min(roi_pct / 100 * 100, 100)
        bsr_factor = max(0, (1 - bsr_rank / bsr_category_max)) * 100 if bsr_category_max > 0 else 50
        competition_factor = max(0, 100 - (num_fba_sellers - 1) * 15)
        stability_score = max(0, 100 - price_volatility_30d * 500)
        price_stability_factor = min(stability_score, 100)
        avail_base = 100 if in_stock else 30
        if buy_box_stable:
            avail_base = min(avail_base + 10, 100)
        availability_factor = avail_base

        composite = (
            roi_factor * self.WEIGHTS["roi"]
            + bsr_factor * self.WEIGHTS["bsr"]
            + competition_factor * self.WEIGHTS["competition"]
            + price_stability_factor * self.WEIGHTS["price_stability"]
            + availability_factor * self.WEIGHTS["availability"]
        )
        composite_score = int(min(max(composite, 0), 100))

        label = "C PASS"
        for (low, high), lbl in self.LABELS.items():
            if low <= composite_score < high:
                label = lbl
                break

        return ScoreBreakdown(
            roi_factor=round(roi_factor, 1),
            bsr_factor=round(bsr_factor, 1),
            competition_factor=round(competition_factor, 1),
            price_stability_factor=round(price_stability_factor, 1),
            availability_factor=round(availability_factor, 1),
            composite_score=composite_score,
            score_label=label,
        )
