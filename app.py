import streamlit as st
import pandas as pd
from utils import CSS_STYLES, load_data

st.set_page_config(
    page_title="MGH Hospital Analytics",
    page_icon=":material/local_hospital:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CSS_STYLES, unsafe_allow_html=True)

encounters, patients, payers, procedures, missing_files = load_data()

if missing_files:
    st.error(f"CSV files not found: {', '.join(missing_files)}")
    st.stop()

st.session_state["encounters"] = encounters
st.session_state["patients"] = patients
st.session_state["payers"] = payers
st.session_state["procedures"] = procedures

with st.sidebar:
    st.title(":material/local_hospital: MGH Analytics")
    st.caption("Massachusetts General Hospital")
    st.divider()

    min_year = int(encounters["YEAR"].min())
    max_year = int(encounters["YEAR"].max())
    selected_years = st.slider("Year Range", min_year, max_year, (min_year, max_year))

    all_payers = sorted(encounters["PAYER_NAME"].unique().tolist())
    selected_payers = st.multiselect("Payer", all_payers, default=all_payers)

    all_classes = sorted(encounters["ENCOUNTERCLASS"].unique().tolist())
    selected_classes = st.multiselect(
        "Encounter Class", all_classes, default=all_classes
    )

    st.divider()
    st.info("**Data Range:** Jan 2, 2011 - Feb 5, 2022\n\nPatient data from classroom.")
    st.divider()
    st.markdown(
        ":material/code: [streamlit-echarts](https://github.com/0xkeonho/dashboard-ets/)"
    )

st.session_state["selected_years"] = selected_years
st.session_state["selected_payers"] = selected_payers
st.session_state["selected_classes"] = selected_classes

pg = st.navigation(
    [
        st.Page(
            "pages/dashboard_overview.py",
            title="Dashboard Overview",
            icon=":material/dashboard:",
            default=True,
        ),
        st.Page(
            "pages/encounters_analysis.py",
            title="Encounters Analysis",
            icon=":material/swap_horiz:",
        ),
        st.Page(
            "pages/financials_coverage.py",
            title="Financials & Coverage",
            icon=":material/payments:",
        ),
        st.Page(
            "pages/patient_behavior.py",
            title="Patient Behavior",
            icon=":material/groups:",
        ),
    ]
)
pg.run()
