import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from common import require_data

st.set_page_config(page_title="SKU Deep Dive", layout="wide")
risk, forecast, weekly, master, inventory, sku_master = require_data()

st.title("SKU Deep Dive")

sku_id = st.selectbox("Choose a SKU", sorted(sku_master["sku_id"].unique()))

info = sku_master[sku_master["sku_id"] == sku_id].iloc[0]
st.subheader(f"{info['sku_name']} ({sku_id})")
st.write(f"**Category:** {info['category']} / {info['subcategory']}  |  **Brand:** {info['brand']}")

r = risk[risk["sku_id"] == sku_id]
if not r.empty:
    r = r.iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Quadrant", r["quadrant"])
    col2.metric("Weeks of cover", f"{r['weeks_of_cover']:.1f}" if r["weeks_of_cover"] == r["weeks_of_cover"] else "N/A")
    col3.metric("Stockout risk", f"{r['stockout_risk']:.0%}")
    col4.metric("Overstock risk", f"{r['overstock_risk']:.0%}")
else:
    st.warning("No inventory/risk data for this SKU.")

hist = weekly[weekly["sku_id"] == sku_id][["week_start", "units_sold"]].set_index("week_start")
st.line_chart(hist)