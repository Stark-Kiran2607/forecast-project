import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from common import require_data

st.set_page_config(page_title="Category Trends", layout="wide")
risk, forecast, weekly, *_ = require_data()

st.title("Category Trends")

category = st.selectbox("Category", sorted(weekly["category"].dropna().unique()))
cat_weekly = weekly[weekly["category"] == category].groupby("week_start")["units_sold"].sum()
st.area_chart(cat_weekly)
st.caption(f"Total units sold, {category}, all SKUs combined.")