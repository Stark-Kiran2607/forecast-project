import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from common import require_data

st.set_page_config(page_title="Top Movers", layout="wide")
risk, forecast, weekly, master, inventory, sku_master = require_data()

st.title("Top Movers")

n = st.slider("How many SKUs to show", 5, 50, 10)
totals = (
    weekly.groupby(["sku_id", "category"], as_index=False)["units_sold"]
    .sum()
    .sort_values("units_sold", ascending=False)
    .head(n)
)
st.bar_chart(totals.set_index("sku_id")["units_sold"])
st.dataframe(totals, use_container_width=True)