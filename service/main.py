"""
FORESIGHT — Scoring Service (FastAPI)
Serves precomputed forecast + risk for a given SKU (or a batch).
Run with: uvicorn service.main:app --reload
"""
from pathlib import Path
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"

app = FastAPI(title="FORESIGHT Scoring Service", version="1.0")

_risk_df: Optional[pd.DataFrame] = None
_forecast_df: Optional[pd.DataFrame] = None


def get_data():
    """Load processed data lazily and cache in memory. Raises a clear error
    if the upstream notebooks haven't been run yet, instead of crashing."""
    global _risk_df, _forecast_df
    if _risk_df is None:
        risk_path = PROCESSED_DIR / "risk_scoring.csv"
        forecast_path = PROCESSED_DIR / "forward_forecast.csv"
        if not risk_path.exists() or not forecast_path.exists():
            raise HTTPException(
                status_code=503,
                detail="Scoring data not found — run the Week 1-3 pipeline/notebooks first.",
            )
        _risk_df = pd.read_csv(risk_path)
        _forecast_df = pd.read_csv(forecast_path, parse_dates=["week_start"])
    return _risk_df, _forecast_df


class WeeklyForecast(BaseModel):
    week_start: str
    forecast_units: float


class SkuScore(BaseModel):
    sku_id: str
    category: Optional[str] = None
    forecast_horizon_units: Optional[float] = None
    weekly_forecast: List[WeeklyForecast] = []
    stock_on_hand: Optional[float] = None
    weeks_of_cover: Optional[float] = None
    stockout_risk: Optional[float] = None
    overstock_risk: Optional[float] = None
    quadrant: Optional[str] = None
    rupee_at_risk_stockout: Optional[float] = None
    rupee_locked_overstock: Optional[float] = None


def _score_one(sku_id: str, risk_df: pd.DataFrame, forecast_df: pd.DataFrame) -> SkuScore:
    row = risk_df[risk_df["sku_id"] == sku_id]
    if row.empty:
        raise HTTPException(status_code=404, detail=f"Unknown sku_id: {sku_id}")
    row = row.iloc[0]

    weekly = forecast_df[forecast_df["sku_id"] == sku_id].sort_values("week_start")
    weekly_list = [
        WeeklyForecast(week_start=str(r["week_start"].date()), forecast_units=round(r["forecast"], 2))
        for _, r in weekly.iterrows()
    ]

    def safe(val):
        return None if pd.isna(val) else float(val)

    return SkuScore(
        sku_id=sku_id,
        category=row.get("category"),
        forecast_horizon_units=safe(row.get("forecast_horizon_units")),
        weekly_forecast=weekly_list,
        stock_on_hand=safe(row.get("stock_on_hand")),
        weeks_of_cover=safe(row.get("weeks_of_cover")),
        stockout_risk=safe(row.get("stockout_risk")),
        overstock_risk=safe(row.get("overstock_risk")),
        quadrant=row.get("quadrant"),
        rupee_at_risk_stockout=safe(row.get("rupee_at_risk_stockout")),
        rupee_locked_overstock=safe(row.get("rupee_locked_overstock")),
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/score/{sku_id}", response_model=SkuScore)
def score_sku(sku_id: str):
    """Forecast + risk for a single SKU."""
    risk_df, forecast_df = get_data()
    return _score_one(sku_id, risk_df, forecast_df)


class BatchRequest(BaseModel):
    sku_ids: List[str]


@app.post("/score/batch", response_model=List[SkuScore])
def score_batch(request: BatchRequest):
    """Forecast + risk for a batch of SKUs. Unknown SKUs are skipped, not
    crashed on, since one bad ID in a batch shouldn't fail the whole request."""
    risk_df, forecast_df = get_data()
    results = []
    for sku_id in request.sku_ids:
        try:
            results.append(_score_one(sku_id, risk_df, forecast_df))
        except HTTPException:
            continue
    return results