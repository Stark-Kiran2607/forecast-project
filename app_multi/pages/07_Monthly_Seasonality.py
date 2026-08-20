import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import altair as alt
import pandas as pd
import streamlit as st
from common import require_data

st.set_page_config(page_title="Monthly Seasonality", layout="wide")
*_, master, _, _ = require_data()

st.title("Seasonality — by Month")
st.caption("Index: 100 = yearly average demand. Hover a bar for the exact value.")

monthly = master.groupby(master["date"].dt.month)["units_sold"].sum()
index_df = (monthly / monthly.mean() * 100).round(1).reset_index()
index_df.columns = ["month", "seasonality_index"]

month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
index_df["month_name"] = index_df["month"].apply(lambda m: month_names[m - 1])

chart = (
    alt.Chart(index_df)
    .mark_bar()
    .encode(
        x=alt.X("month_name", sort=month_names, title="Month"),
        y=alt.Y("seasonality_index", title="Seasonality index"),
        tooltip=["month_name", "seasonality_index"],
        color=alt.condition(
            alt.datum.seasonality_index > 100, alt.value("#2ecc71"), alt.value("#e74c3c")
        ),
    )
)
st.altair_chart(chart, use_container_width=True)