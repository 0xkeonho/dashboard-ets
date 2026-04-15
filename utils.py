import sys
import os

# ==========================================
# 1. STREAMLIT NATIVE THEME CONFIGURATION
# ==========================================
os.makedirs(".streamlit", exist_ok=True)
config_path = ".streamlit/config.toml"
with open(config_path, "w") as f:
    f.write("""[theme]
base="light"
primaryColor="#8b5cf6"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f8fafc"
textColor="#1e293b"
font="sans serif"
baseRadius = "12px"

[theme.sidebar]
backgroundColor = "#1e293b"
textColor = "#f1f5f9"
secondaryBackgroundColor = "#334155"
""")

# ==========================================
# FIX FOR PLOTLY ORJSON ERROR
# ==========================================
sys.modules["orjson"] = None

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_echarts import st_echarts, JsCode

# ==========================================
# 2. CSS STYLES
# ==========================================
CSS_STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* Main Content - White Background */
.main, .stApp { background-color: #ffffff !important; }
[data-testid="stMainBlockContainer"] { background-color: #ffffff !important; }

/* DO NOT TOUCH PLOTLY CHARTS */
.js-plotly-plot, .plotly, .modebar, .plot-container,
[data-testid="stPlotlyChart"], .stPlotlyChart {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}

/* Material Icons */
.material-icons, .material-symbols-rounded, span.material-symbols-rounded {
    font-family: 'Material Symbols Rounded' !important;
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}

/* Global Font (Poppins) - ONLY text elements */
html, body, p, h1, h2, h3, h4, h5, h6, label, li, a, button, th, td {
    font-family: 'Poppins', sans-serif !important;
}

/* Sidebar - Dark Theme */
section[data-testid="stSidebar"] { background-color: #1e293b !important; }
section[data-testid="stSidebar"] > div > div { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] h1 { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] h2 { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] h4 { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] label { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] p { color: #f1f5f9 !important; }
section[data-testid="stSidebar"] .stRadio > label {
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] .stRadio div {
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] [data-baseweb="radio"] {
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] [data-baseweb="radio"] * {
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: #334155 !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] .stSlider label {
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {
    background-color: #334155 !important;
}
section[data-testid="stSidebar"] input {
    background-color: #334155 !important;
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] .stCaption {
    color: #94a3b8 !important;
}
section[data-testid="stSidebar"] [data-testid="stInfo"] {
    background-color: #334155 !important;
    color: #f1f5f9 !important;
}
section[data-testid="stSidebar"] [data-testid="stInfo"] * {
    color: #f1f5f9 !important;
}

/* Light Theme Headers (Main Content) */
.main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
    font-weight: 700 !important;
    color: #1e293b !important;
}

h1 { font-size: 2.2rem !important; margin-bottom: 0.2rem !important; }
h2 { font-size: 1.5rem !important; margin-top: 1.5rem !important; margin-bottom: 1rem !important; }
h3 { font-size: 1.2rem !important; margin-top: 1.2rem !important; margin-bottom: 0.8rem !important; }

/* Subtitle / Caption styling */
.page-subtitle {
    font-size: 1rem;
    color: #64748b;
    margin-bottom: 2rem;
    font-weight: 400;
    font-family: 'Poppins', sans-serif !important;
}

/* Premium KPI Cards - Light Theme */
.kpi-container {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    font-family: 'Poppins', sans-serif !important;
}
.kpi-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    flex: 1;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
    font-family: 'Poppins', sans-serif !important;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.kpi-title {
    font-size: 0.85rem;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.5px;
    font-family: 'Poppins', sans-serif !important;
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 8px 0;
    line-height: 1.2;
    font-family: 'Poppins', sans-serif !important;
}

/* Colors */
.val-green { color: #10b981; }
.val-blue  { color: #3b82f6; }
.val-amber { color: #f59e0b; }
.val-red   { color: #ef4444; }

/* Insight Box - Light Theme */
.insight-box {
    background-color: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-left: 4px solid #10b981;
    padding: 16px 20px;
    border-radius: 8px;
    margin-top: 1rem;
    font-size: 0.95rem;
    color: #1e293b;
    line-height: 1.6;
}
.insight-box strong { color: #059669; font-weight: 600; }
</style>
"""

# ==========================================
# 3. CONSTANTS
# ==========================================
CHART_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "scrollZoom": True,
    "toImageButtonOptions": {"format": "png", "filename": "mgh_analytics_export"},
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
}

CHART_CONFIG_ZOOM = {
    "displayModeBar": True,
    "displaylogo": False,
    "scrollZoom": True,
    "toImageButtonOptions": {"format": "png", "filename": "mgh_analytics_export"},
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "modeBarButtonsToAdd": ["drawrect", "eraseshape"],
}

DISCRETE_COLORS = ["#00c9a7", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6", "#10b981"]

ECHARTS_BASE = {
    "backgroundColor": "#ffffff",
    "textStyle": {"color": "#1e293b", "fontFamily": "Poppins"},
}

PAYER_TYPE = {
    "Medicare": "Government (65+)",
    "Medicaid": "Government (Low-income)",
    "Dual Eligible": "Government (Medicare + Medicaid)",
    "Blue Cross Blue Shield": "Private Insurance",
    "UnitedHealthcare": "Private Insurance",
    "Aetna": "Private Insurance",
    "Cigna Health": "Private Insurance",
    "Anthem": "Private Insurance",
    "Humana": "Private Insurance",
    "NO_INSURANCE": "Self-pay (No Insurance)",
}


# ==========================================
# 4. DATA LOADING
# ==========================================
@st.cache_data(show_spinner=False)
def load_data():
    DATA_PATH = "data"
    required_files = [
        os.path.join(DATA_PATH, "encounters.csv"),
        os.path.join(DATA_PATH, "patients.csv"),
        os.path.join(DATA_PATH, "payers.csv"),
        os.path.join(DATA_PATH, "procedures.csv"),
    ]
    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        return None, None, None, None, missing_files

    encounters = pd.read_csv(required_files[0])
    patients = pd.read_csv(required_files[1])
    payers = pd.read_csv(required_files[2])
    procedures = pd.read_csv(required_files[3])

    # Date Preprocessing
    encounters["START"] = pd.to_datetime(encounters["START"]).dt.tz_localize(None)
    encounters["STOP"] = pd.to_datetime(encounters["STOP"]).dt.tz_localize(None)
    encounters["YEAR"] = encounters["START"].dt.year
    encounters["MONTH"] = encounters["START"].dt.month
    encounters["QUARTER"] = encounters["START"].dt.to_period("Q").astype(str)

    # Standardize Encounter Class naming format
    encounters["ENCOUNTERCLASS"] = (
        encounters["ENCOUNTERCLASS"].str.title().replace("Urgentcare", "Urgent Care")
    )

    # Calculate duration
    encounters["DURATION_HOURS"] = (
        encounters["STOP"] - encounters["START"]
    ).dt.total_seconds() / 3600
    encounters["IS_OVER_24H"] = encounters["DURATION_HOURS"] > 24

    # 30-Day Readmission Identification
    encounters = encounters.sort_values(["PATIENT", "START"])
    encounters["PREV_STOP"] = encounters.groupby("PATIENT")["STOP"].shift(1)
    encounters["DAYS_TO_READMIT"] = (
        encounters["START"] - encounters["PREV_STOP"]
    ).dt.total_seconds() / 86400
    encounters["IS_READMIT_30D"] = (encounters["DAYS_TO_READMIT"] >= 0) & (
        encounters["DAYS_TO_READMIT"] <= 30
    )

    # Merge Payer Name (Prevent overlap)
    encounters = encounters.merge(
        payers[["Id", "NAME"]],
        left_on="PAYER",
        right_on="Id",
        how="left",
        suffixes=("", "_PAYER"),
    )
    encounters.rename(columns={"NAME": "PAYER_NAME"}, inplace=True)
    encounters["PAYER_NAME"] = encounters["PAYER_NAME"].fillna("Unknown Payer")

    return encounters, patients, payers, procedures, []


# ==========================================
# 5. HELPER FUNCTIONS
# ==========================================
def style_plotly(fig, add_zoom=False, x_title=None, y_title=None):
    fig.update_layout(
        font_family="Poppins",
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        hoverlabel=dict(
            bgcolor="#ffffff", font_size=13, font_family="Poppins", font_color="#1e293b"
        ),
        margin=dict(l=10, r=10, t=40, b=10),
    )

    xaxis_config = {
        "showgrid": False,
        "zeroline": False,
    }
    if x_title:
        xaxis_config["title_text"] = x_title
        xaxis_config["title_font"] = dict(size=13, color="#1e293b")
    if add_zoom:
        xaxis_config["rangeslider"] = dict(
            visible=True, bgcolor="#f1f5f9", thickness=0.15
        )
    fig.update_xaxes(**xaxis_config)

    yaxis_config = {
        "showgrid": True,
        "gridwidth": 1,
        "gridcolor": "#e2e8f0",
        "zeroline": False,
    }
    if y_title:
        yaxis_config["title_text"] = y_title
        yaxis_config["title_font"] = dict(size=13, color="#1e293b")
    fig.update_yaxes(**yaxis_config)

    return fig


def get_sparkline_data(df, value_col, agg_type="sum", group_col="YEAR"):
    if df.empty:
        return None
    if agg_type == "count":
        trend = df.groupby(group_col).size().reset_index(name="value")
    elif agg_type == "nunique":
        trend = df.groupby(group_col)[value_col].nunique().reset_index(name="value")
    elif agg_type == "mean":
        trend = df.groupby(group_col).agg({value_col: "mean"}).reset_index()
        trend.rename(columns={value_col: "value"}, inplace=True)
    else:
        trend = df.groupby(group_col).agg({value_col: "sum"}).reset_index()
        trend.rename(columns={value_col: "value"}, inplace=True)
    trend = trend.sort_values(group_col)
    return trend["value"].tolist()


def calc_delta(current_val, previous_val):
    if previous_val is None or previous_val == 0:
        return None
    delta_pct = ((current_val - previous_val) / previous_val) * 100
    return f"{delta_pct:+.1f}%"


# ==========================================
# 6. SIDEBAR FILTERS
# ==========================================
def render_sidebar_filters(encounters):
    st.sidebar.title(":material/local_hospital: MGH Analytics")
    st.sidebar.caption("Massachusetts General Hospital")
    st.sidebar.divider()

    min_year = int(encounters["YEAR"].min())
    max_year = int(encounters["YEAR"].max())
    selected_years = st.sidebar.slider(
        "Year Range", min_year, max_year, (min_year, max_year)
    )

    all_payers = sorted(encounters["PAYER_NAME"].unique().tolist())
    selected_payers = st.sidebar.multiselect("Payer", all_payers, default=all_payers)

    all_classes = sorted(encounters["ENCOUNTERCLASS"].unique().tolist())
    selected_classes = st.sidebar.multiselect(
        "Encounter Class", all_classes, default=all_classes
    )

    st.sidebar.divider()
    st.sidebar.info(
        "**Data Range:** Jan 2, 2011 - Feb 5, 2022\n\nPatient data from classroom."
    )
    st.sidebar.divider()
    st.sidebar.markdown(
        ":material/code: [streamlit-echarts](https://github.com/0xkeonho/dashboard-ets/)"
    )

    return selected_years, selected_payers, selected_classes


def apply_filters(
    encounters, procedures, selected_years, selected_payers, selected_classes
):
    """Apply filters to dataframes."""
    filtered_encounters = encounters[
        (encounters["YEAR"] >= selected_years[0])
        & (encounters["YEAR"] <= selected_years[1])
        & (encounters["PAYER_NAME"].isin(selected_payers))
        & (encounters["ENCOUNTERCLASS"].isin(selected_classes))
    ]

    valid_encounter_ids = filtered_encounters["Id"].tolist()
    filtered_procedures = procedures[procedures["ENCOUNTER"].isin(valid_encounter_ids)]

    return filtered_encounters, filtered_procedures
