import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st
from common import require_data

st.set_page_config(page_title="Dead Stock", layout="wide")
risk, forecast, weekly, master, inventory, sku_master = require_data()

st.title("Dead Stock")

recent_weeks = st.slider("Look-back window (weeks)", 4, 16, 8)
threshold = st.slider("Max units sold in that window to count as dead", 0, 20, 5)

cutoff = weekly["week_start"].max() - pd.Timedelta(weeks=recent_weeks)
recent = weekly[weekly["week_start"] > cutoff]
recent_totals = recent.groupby(["sku_id", "category"], as_index=False)["units_sold"].sum()
dead = recent_totals[recent_totals["units_sold"] <= threshold].sort_values("units_sold")

st.metric("Dead-stock SKUs", len(dead))
if not dead.empty:
    st.bar_chart(dead.set_index("sku_id")["units_sold"])
st.dataframe(dead, use_container_width=True)