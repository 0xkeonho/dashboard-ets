import streamlit as st
from utils import CSS_STYLES

st.set_page_config(
    page_title="MGH Hospital Analytics",
    page_icon=":material/local_hospital:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CSS_STYLES, unsafe_allow_html=True)

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

st.markdown(CSS_STYLES, unsafe_allow_html=True)

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

with st.sidebar:
    st.markdown(
        ":material/code: [streamlit-echarts](https://github.com/0xkeonho/dashboard-ets/)"
    )
