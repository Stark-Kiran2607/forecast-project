"""
Shared data-loading for all dashboard pages.
Every page imports load_data() from here instead of re-reading CSVs,
so there's exactly one place that knows where the files live.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"


@st.cache_data
def load_data():
    risk = pd.read_csv(PROCESSED_DIR / "risk_scoring.csv")
    forecast = pd.read_csv(PROCESSED_DIR / "forward_forecast.csv", parse_dates=["week_start"])
    weekly = pd.read_csv(PROCESSED_DIR / "weekly_sales.csv", parse_dates=["week_start"])
    master = pd.read_csv(PROCESSED_DIR / "master_dataset.csv", parse_dates=["date"])
    inventory = pd.read_csv(PROCESSED_DIR / "inventory_position.csv")
    sku_master = pd.read_csv(PROCESSED_DIR / "sku_master.csv")
    return risk, forecast, weekly, master, inventory, sku_master


def require_data():
    """Every page calls this first. Fails loudly and clearly instead of a
    raw traceback if Weeks 1-3 haven't been run yet."""
    try:
        return load_data()
    except FileNotFoundError as e:
        st.error(f"Missing processed data: {e}. Run the Week 1-3 notebooks first.")
        st.stop()