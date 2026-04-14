import streamlit as st
import pandas as pd
from utils import CSS_STYLES, load_data

st.set_page_config(
    page_title="MGH Hospital Analytics",
    page_icon=":material/local_hospital:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Dashboard Dataset Case 2 - Project Dashboard ETS"},
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

PAGES = {
    "Dashboard Overview": "pages/dashboard_overview.py",
    "Encounters Analysis": "pages/encounters_analysis.py",
    "Financials & Coverage": "pages/financials_coverage.py",
    "Patient Behavior": "pages/patient_behavior.py",
}

PAGE_ICONS = {
    "Dashboard Overview": ":material/dashboard:",
    "Encounters Analysis": ":material/swap_horiz:",
    "Financials & Coverage": ":material/payments:",
    "Patient Behavior": ":material/groups:",
}

with st.sidebar:
    st.title(":material/local_hospital: MGH Analytics")
    st.caption("Massachusetts General Hospital")
    st.divider()

    page_selection = st.radio(
        "Navigation",
        list(PAGES.keys()),
        format_func=lambda x: f"{PAGE_ICONS[x]} {x}",
        label_visibility="collapsed",
    )

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
        ":material/code: [GitHub - dashboard-ets](https://github.com/0xkeonho/dashboard-ets/)"
    )

st.session_state["selected_years"] = selected_years
st.session_state["selected_payers"] = selected_payers
st.session_state["selected_classes"] = selected_classes

page_file = PAGES[page_selection]
with open(page_file, "r") as f:
    code = compile(f.read(), page_file, "exec")
    exec(code)
