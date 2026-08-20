import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import plotly.express as px
import streamlit as st
from common import require_data

st.set_page_config(page_title="Rupee Impact", layout="wide")
risk, forecast, weekly, master, inventory, sku_master = require_data()

st.title("Rupee Impact")

col1, col2 = st.columns(2)
col1.metric("Total revenue at risk (stockouts)", f"₹{risk['rupee_at_risk_stockout'].sum():,.0f}")
col2.metric("Total capital locked (overstock)", f"₹{risk['rupee_locked_overstock'].sum():,.0f}")

st.subheader("Exposure per SKU — hover for details")
fig = px.scatter(
    risk,
    x="rupee_at_risk_stockout",
    y="rupee_locked_overstock",
    color="quadrant",
    hover_name="sku_id",
    hover_data=["category", "weeks_of_cover"],
    labels={
        "rupee_at_risk_stockout": "Revenue at risk (₹)",
        "rupee_locked_overstock": "Capital locked (₹)",
    },
)
st.plotly_chart(fig, use_container_width=True)