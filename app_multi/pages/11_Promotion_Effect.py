import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st
from common import require_data

st.set_page_config(page_title="Promotion Effect", layout="wide")
risk, forecast, weekly, master, inventory, sku_master = require_data()

st.title("Promotion Effect")
st.caption("Naive comparison, not causal — promo days may also be seasonally busier.")

promo_avg = master.loc[master["promo_flag"], "units_sold"].mean()
non_promo_avg = master.loc[~master["promo_flag"], "units_sold"].mean()
lift_pct = (promo_avg / non_promo_avg - 1) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Avg units/day, promo", f"{promo_avg:.1f}")
col2.metric("Avg units/day, non-promo", f"{non_promo_avg:.1f}")
col3.metric("Apparent lift", f"{lift_pct:.1f}%")

compare = pd.Series({"Promo days": promo_avg, "Non-promo days": non_promo_avg})
st.bar_chart(compare)