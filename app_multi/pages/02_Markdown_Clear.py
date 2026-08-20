import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from common import require_data

st.set_page_config(page_title="Markdown / Clear", layout="wide")
risk, *_ = require_data()

st.title("Markdown / Clear")
st.caption("High overstock risk, low stockout risk — promote or discount to free up capital.")

table = risk[risk["quadrant"] == "Markdown / Clear"].sort_values("rupee_locked_overstock", ascending=False)
if table.empty:
    st.success("No SKUs currently need markdown.")
else:
    st.metric("SKUs to markdown", len(table))
    st.bar_chart(table.set_index("sku_id")["rupee_locked_overstock"])
    st.dataframe(
        table[["sku_id", "category", "stock_on_hand", "weeks_of_cover", "overstock_risk", "rupee_locked_overstock"]],
        use_container_width=True,
    )