import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st
from common import require_data

st.set_page_config(page_title="Forecast vs Actual", layout="wide")
risk, forecast, weekly, *_ = require_data()

st.title("Forecast vs Actual")

sku_id = st.selectbox("Choose a SKU", sorted(weekly["sku_id"].unique()))

hist = weekly[weekly["sku_id"] == sku_id][["week_start", "units_sold"]].rename(columns={"units_sold": "Actual"})
fut = forecast[forecast["sku_id"] == sku_id][["week_start", "forecast"]].rename(columns={"forecast": "Forecast"})

if hist.empty and fut.empty:
    st.warning("No data for this SKU.")
else:
    chart = pd.concat([hist.set_index("week_start"), fut.set_index("week_start")], axis=1)
    st.line_chart(chart)