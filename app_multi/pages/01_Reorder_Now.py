import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from common import require_data

st.set_page_config(page_title="Reorder Now", layout="wide")
risk, *_ = require_data()

st.title("Reorder Now")
st.caption("High stockout risk, low overstock risk — raise a replenishment order.")

table = risk[risk["quadrant"] == "Reorder Now"].sort_values("rupee_at_risk_stockout", ascending=False)
if table.empty:
    st.success("No SKUs currently need reordering.")
else:
    st.metric("SKUs to reorder", len(table))
    st.bar_chart(table.set_index("sku_id")["rupee_at_risk_stockout"])
    st.dataframe(
        table[["sku_id", "category", "stock_on_hand", "weeks_of_cover", "stockout_risk", "rupee_at_risk_stockout"]],
        use_container_width=True,
    )