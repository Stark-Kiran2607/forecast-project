import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from common import require_data

st.set_page_config(page_title="Inventory Position", layout="wide")
risk, forecast, weekly, master, inventory, sku_master = require_data()

st.title("Inventory Position")
st.caption("Point-in-time stock snapshot, aggregated across all stores per SKU.")

category = st.selectbox("Category", ["All"] + sorted(inventory["category"].dropna().unique().tolist()))
table = inventory if category == "All" else inventory[inventory["category"] == category]

st.scatter_chart(table, x="reorder_point", y="stock_on_hand", color="category")
st.caption("Points below the diagonal are under their reorder point.")

st.dataframe(
    table[["sku_id", "category", "stock_on_hand", "reorder_point", "safety_stock", "n_stores_carrying"]],
    use_container_width=True,
)