import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

REPORT_PATH = Path(__file__).resolve().parent.parent.parent / "reports" / "data_quality_report.md"

st.set_page_config(page_title="Data Quality", layout="wide")
st.title("Data Quality Report")

if REPORT_PATH.exists():
    st.markdown(REPORT_PATH.read_text(encoding="utf-8"))
else:
    st.warning("No data quality report found — run the Week 1 notebook first.")