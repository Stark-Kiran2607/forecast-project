import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import streamlit as st
from common import require_data

st.set_page_config(page_title="Healthy SKUs", layout="wide")
risk, *_ = require_data()

st.title("Healthy")
st.caption("Low risk on both axes — no action needed, leave as is.")

table = risk[risk["quadrant"] == "Healthy"]
st.metric("Healthy SKUs", len(table))

fig, ax = plt.subplots()
ax.hist(table["weeks_of_cover"].dropna(), bins=20, color="#2ecc71", edgecolor="white")
ax.set_xlabel("Weeks of cover")
ax.set_ylabel("Number of SKUs")
ax.set_title("Distribution of stock cover among healthy SKUs")
st.pyplot(fig)

st.dataframe(table[["sku_id", "category", "stock_on_hand", "weeks_of_cover"]], use_container_width=True)