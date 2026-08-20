import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from common import require_data

st.set_page_config(page_title="Watch / Volatile", layout="wide")
risk, *_ = require_data()

st.title("Watch / Volatile")
st.caption("High risk on both stockout and overstock — demand is erratic, review manually.")

table = risk[risk["quadrant"] == "Watch / Volatile"]
if table.empty:
    st.info("No SKUs currently in this quadrant.")
else:
    st.metric("SKUs to investigate", len(table))
    st.scatter_chart(table, x="overstock_risk", y="stockout_risk", size="rupee_at_risk_stockout")
    st.dataframe(
        table[["sku_id", "category", "stockout_risk", "overstock_risk", "weeks_of_cover"]],
        use_container_width=True,
    )