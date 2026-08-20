"""Page 1 — Overview. Run with: streamlit run app_multi/Home.py"""
import streamlit as st
from common import require_data

st.set_page_config(page_title="FORESIGHT — Overview", layout="wide")
risk, forecast, weekly, master, inventory, sku_master = require_data()

st.title("FORESIGHT — Demand & Inventory Intelligence")
st.caption("NorthBay Living — Overview")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Active SKUs", len(risk))
col2.metric("Reorder now", (risk["quadrant"] == "Reorder Now").sum())
col3.metric("Markdown / clear", (risk["quadrant"] == "Markdown / Clear").sum())
col4.metric("Revenue at risk (₹)", f"{risk['rupee_at_risk_stockout'].sum():,.0f}")
col5.metric("Capital locked (₹)", f"{risk['rupee_locked_overstock'].sum():,.0f}")

st.divider()
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("Risk breakdown")
    st.bar_chart(risk["quadrant"].value_counts())
with col_right:
    st.subheader("Total demand trend")
    total_weekly = weekly.groupby("week_start")["units_sold"].sum()
    st.area_chart(total_weekly)

