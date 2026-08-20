import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import plotly.express as px
import streamlit as st
from common import require_data

st.set_page_config(page_title="Decisioning Grid", layout="wide")
risk, *_ = require_data()

st.title("Decisioning Grid")
st.caption("Every SKU plotted by stockout risk vs overstock risk. Hover for SKU details.")

# SKUs with no inventory match (see Week 1 data-quality report) have NaN
# rupee_at_risk_stockout — Plotly's size parameter can't plot NaN, so fill
# with 0 just for the plot (the underlying data stays untouched).
plot_data = risk.copy()
plot_data["bubble_size"] = plot_data["rupee_at_risk_stockout"].fillna(0)

fig = px.scatter(
    plot_data,
    x="overstock_risk",
    y="stockout_risk",
    color="quadrant",
    size="bubble_size",
    hover_name="sku_id",
    hover_data=["category", "weeks_of_cover"],
)
fig.add_hline(y=0.5, line_dash="dot", line_color="gray")
fig.add_vline(x=0.5, line_dash="dot", line_color="gray")
st.plotly_chart(fig, use_container_width=True)