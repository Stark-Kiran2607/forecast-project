import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from common import require_data

st.set_page_config(page_title="Weekday Seasonality", layout="wide")
*_, master, _, _ = require_data()

st.title("Seasonality — by Weekday")
st.caption("Index: 100 = weekly average demand.")

order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow = master.groupby(master["date"].dt.day_name())["units_sold"].sum().reindex(order)
index = (dow / dow.mean() * 100).round(1)
st.bar_chart(index)