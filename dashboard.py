import sys
import os

# ==========================================
# 1. STREAMLIT NATIVE THEME CONFIGURATION
# ==========================================
# Menulis ulang file konfigurasi tema Streamlit secara native.
# Ini akan mengatasi masalah UI putih/rusak pada filter sidebar.
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
# 2. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="MGH Hospital Analytics",
    page_icon=":material/local_hospital:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)


# ==========================================
# 4. LOAD & PREP DATA FUNCTION (CACHED)
# ==========================================
@st.cache_data
@st.cache_data
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


# Standard Plotly Configuration
chart_config = {
    "displayModeBar": True,
    "displaylogo": False,
    "scrollZoom": True,
    "toImageButtonOptions": {"format": "png", "filename": "mgh_analytics_export"},
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
}

# Chart config with range slider for time series
chart_config_zoom = {
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


# ==========================================
# 5. LOAD DATA
# ==========================================
encounters, patients, payers, procedures, missing_files = load_data()

if missing_files:
    st.error(f"CSV files not found: {', '.join(missing_files)}")
    st.stop()


# ==========================================
# 6. SIDEBAR (NAVIGATION & FILTERS)
# ==========================================
st.sidebar.title(":material/local_hospital: MGH Analytics")
st.sidebar.caption("Massachusetts General Hospital")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        ":material/dashboard: Dashboard Overview",
        ":material/swap_horiz: Encounters Analysis",
        ":material/payments: Financials & Coverage",
        ":material/groups: Patient Behavior",
    ],
)

st.sidebar.divider()

st.sidebar.subheader(":material/tune: Data Filters")

# 1. Year Filter
min_year = int(encounters["YEAR"].min())
max_year = int(encounters["YEAR"].max())
selected_years = st.sidebar.slider(
    "Select Year Range", min_year, max_year, (min_year, max_year)
)

# 2. Payer Filter
all_payers = sorted(encounters["PAYER_NAME"].unique().tolist())
selected_payers = st.sidebar.multiselect("Select Payer", all_payers, default=all_payers)

# 3. Encounter Class Filter
all_classes = sorted(encounters["ENCOUNTERCLASS"].unique().tolist())
selected_classes = st.sidebar.multiselect(
    "Select Encounter Class", all_classes, default=all_classes
)

st.sidebar.divider()
st.sidebar.info("**Data Range:** 2011 - 2022\n\n*Synthetic dataset based on Synthea.*")


# ==========================================
# 7. APPLY FILTERS
# ==========================================
filtered_encounters = encounters[
    (encounters["YEAR"] >= selected_years[0])
    & (encounters["YEAR"] <= selected_years[1])
    & (encounters["PAYER_NAME"].isin(selected_payers))
    & (encounters["ENCOUNTERCLASS"].isin(selected_classes))
]

valid_encounter_ids = filtered_encounters["Id"].tolist()
filtered_procedures = procedures[procedures["ENCOUNTER"].isin(valid_encounter_ids)]


# ==========================================
# 8. PAGE LOGIC & VISUALIZATION
# ==========================================

# Main KPIs
total_encounters = len(filtered_encounters)
unique_patients = (
    filtered_encounters["PATIENT"].nunique() if not filtered_encounters.empty else 0
)
avg_cost_per_visit = (
    filtered_encounters["TOTAL_CLAIM_COST"].mean()
    if not filtered_encounters.empty
    else 0
)
readmitted_patients_count = (
    filtered_encounters[filtered_encounters["IS_READMIT_30D"]]["PATIENT"].nunique()
    if not filtered_encounters.empty
    else 0
)


def calc_delta(current_val, previous_val):
    if previous_val is None or previous_val == 0:
        return None
    delta_pct = ((current_val - previous_val) / previous_val) * 100
    return f"{delta_pct:+.1f}%"


years_available = sorted(filtered_encounters["YEAR"].unique())
if len(years_available) >= 2:
    current_year = years_available[-1]
    prev_year = years_available[-2]

    curr_enc = filtered_encounters[filtered_encounters["YEAR"] == current_year]
    prev_enc = filtered_encounters[filtered_encounters["YEAR"] == prev_year]

    delta_encounters = calc_delta(len(curr_enc), len(prev_enc))
    delta_patients = calc_delta(
        curr_enc["PATIENT"].nunique(), prev_enc["PATIENT"].nunique()
    )
    delta_cost = calc_delta(
        curr_enc["TOTAL_CLAIM_COST"].mean(), prev_enc["TOTAL_CLAIM_COST"].mean()
    )

    curr_readmit = curr_enc[curr_enc["IS_READMIT_30D"]]["PATIENT"].nunique()
    prev_readmit = prev_enc[prev_enc["IS_READMIT_30D"]]["PATIENT"].nunique()
    delta_readmit = calc_delta(curr_readmit, prev_readmit)
else:
    delta_encounters = delta_patients = delta_cost = delta_readmit = None


def render_kpi_row():
    spark_encounters = (
        get_sparkline_data(filtered_encounters, "Id", agg_type="count") or []
    )
    spark_patients = (
        get_sparkline_data(filtered_encounters, "PATIENT", agg_type="nunique") or []
    )
    spark_cost = [
        round(v)
        for v in (
            get_sparkline_data(filtered_encounters, "TOTAL_CLAIM_COST", agg_type="mean")
            or []
        )
    ]
    spark_readmit = (
        get_sparkline_data(
            filtered_encounters[filtered_encounters["IS_READMIT_30D"]],
            "PATIENT",
            agg_type="nunique",
        )
        or []
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Encounters",
            value=f"{total_encounters:,}",
            delta=delta_encounters,
            border=True,
            chart_data=spark_encounters if len(spark_encounters) > 1 else None,
            chart_type="bar",
        )

    with col2:
        st.metric(
            label="Unique Patients",
            value=f"{unique_patients:,}",
            delta=delta_patients,
            border=True,
            chart_data=spark_patients if len(spark_patients) > 1 else None,
            chart_type="line",
        )

    with col3:
        st.metric(
            label="Avg Cost / Visit",
            value=f"${avg_cost_per_visit:,.0f}",
            delta=delta_cost,
            border=True,
            chart_data=spark_cost if len(spark_cost) > 1 else None,
            chart_type="area",
        )

    with col4:
        st.metric(
            label="30-Day Readmissions",
            value=f"{readmitted_patients_count:,}",
            delta=delta_readmit,
            border=True,
            chart_data=spark_readmit if len(spark_readmit) > 1 else None,
            chart_type="bar",
        )


if filtered_encounters.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# ----------------------------------------
# PAGE 1: OVERVIEW
# ----------------------------------------
if page == ":material/dashboard: Dashboard Overview":
    st.markdown("<h1>Hospital Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-subtitle'>Performance Overview (Filtered Data)</div>",
        unsafe_allow_html=True,
    )

    render_kpi_row()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Monthly Encounter Trend")
        st.caption("Encounter volume for the last 12 months from the most recent data.")

        encounters_sorted = filtered_encounters.sort_values("START")
        latest_date = encounters_sorted["START"].max()
        start_date = latest_date - pd.DateOffset(months=12)
        last_12_months = filtered_encounters[
            (filtered_encounters["START"] >= start_date)
            & (filtered_encounters["START"] <= latest_date)
        ].copy()

        last_12_months["YEAR_MONTH"] = last_12_months["START"].dt.to_period("M")
        monthly_data = (
            last_12_months.groupby("YEAR_MONTH")
            .size()
            .reset_index(name="Total Encounters")
        )
        monthly_data = monthly_data.sort_values("YEAR_MONTH")

        months = [str(m) for m in monthly_data["YEAR_MONTH"].tolist()]
        values = monthly_data["Total Encounters"].tolist()

        echarts_monthly_opts = {
            **ECHARTS_BASE,
            "legend": {"bottom": 5, "textStyle": {"color": "#1e293b"}},
            "toolbox": {
                "feature": {
                    "saveAsImage": {},
                    "dataView": {"readOnly": True},
                    "restore": {},
                    "magicType": {"type": ["line", "bar"]},
                }
            },
            "tooltip": {
                "trigger": "axis",
                "formatter": JsCode(
                    "function(p){ return p[0].name + '<br/>Encounters: ' + p[0].value.toLocaleString(); }"
                ).js_code,
            },
            "xAxis": {
                "type": "category",
                "data": months,
                "axisLabel": {"rotate": 45, "color": "#1e293b"},
                "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
            },
            "yAxis": {
                "type": "value",
                "axisLabel": {"color": "#1e293b"},
                "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
                "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
            },
            "dataZoom": [
                {"type": "inside", "start": 0, "end": 100},
                {"type": "slider", "start": 0, "end": 100, "height": 20, "bottom": 30},
            ],
            "grid": {"bottom": "22%", "left": "8%"},
            "series": [
                {
                    "name": "Total Encounters",
                    "type": "line",
                    "data": values,
                    "smooth": True,
                    "itemStyle": {"color": "#10b981"},
                    "areaStyle": {"opacity": 0.3, "color": "#10b981"},
                    "label": {"show": True, "position": "top", "color": "#1e293b"},
                }
            ],
        }
        st_echarts(
            options=echarts_monthly_opts, height="400px", key="monthly_encounter_trend"
        )

    with col2:
        st.subheader("Encounter Class Distribution")
        st.caption("Breakdown of encounter types by class category.")
        class_dist = filtered_encounters["ENCOUNTERCLASS"].value_counts().reset_index()
        class_dist.columns = ["Encounter Class", "Total Encounters"]
        class_dist = class_dist.sort_values("Total Encounters", ascending=False)

        classes_dist = class_dist["Encounter Class"].tolist()
        counts_dist = class_dist["Total Encounters"].tolist()
        pie_data = [{"name": c, "value": v} for c, v in zip(classes_dist, counts_dist)]

        echarts_class_dist_opts = {
            **ECHARTS_BASE,
            "legend": {
                "orient": "horizontal",
                "bottom": 5,
                "textStyle": {"color": "#1e293b"},
            },
            "toolbox": {
                "feature": {
                    "saveAsImage": {},
                    "dataView": {"readOnly": True},
                    "restore": {},
                }
            },
            "tooltip": {
                "trigger": "item",
                "formatter": JsCode(
                    "function(p){ return p.name + '<br/>' + p.value.toLocaleString() + ' (' + p.percent.toFixed(1) + '%)'; }"
                ).js_code,
            },
            "series": [
                {
                    "name": "Encounter Class",
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "center": ["50%", "45%"],
                    "data": pie_data,
                    "itemStyle": {
                        "borderRadius": 6,
                        "borderColor": "#ffffff",
                        "borderWidth": 3,
                    },
                    "label": {
                        "show": True,
                        "formatter": "{b}: {d}%",
                        "color": "#1e293b",
                    },
                    "emphasis": {
                        "label": {"show": True, "fontSize": 14, "fontWeight": "bold"},
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        },
                    },
                }
            ],
            "color": DISCRETE_COLORS,
        }
        st_echarts(
            options=echarts_class_dist_opts,
            height="400px",
            key="encounter_class_distribution",
        )


# ----------------------------------------
# PAGE 2: ENCOUNTERS (SQL OBJECTIVE 1)
# ----------------------------------------
elif page == ":material/swap_horiz: Encounters Analysis":
    st.markdown("<h1>Encounters & Visits</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-subtitle'>Volume trends, service proportions, and durations.</div>",
        unsafe_allow_html=True,
    )

    with st.expander(":material/info: Encounter Class Definitions"):
        st.markdown(
            """
| Class | Definisi |
|-------|----------|
| **Ambulatory** | Kunjungan rawat jalan untuk konsultasi/prosedur tanpa menginap |
| **Emergency** | Kondisi darurat yang mengancam nyawa, membutuhkan penanganan segera |
| **Inpatient** | Rawat inap - pasien menginap di rumah sakit untuk perawatan |
| **Outpatient** | Rawat jalan terjadwal untuk prosedur tanpa menginap |
| **Urgent Care** | Kondisi serius yang membutuhkan penanganan cepat (bukan darurat) |
| **Wellness** | Kunjungan kesehatan rutin - check-up, vaksinasi, skrining preventif |
"""
        )

    st.subheader("Annual Visit Volume")
    st.caption("Yearly encounter counts from 2011 to 2022.")
    enc_year = (
        filtered_encounters.groupby("YEAR").size().reset_index(name="Total Encounters")
    )
    enc_year.rename(columns={"YEAR": "Year"}, inplace=True)

    years = enc_year["Year"].astype(str).tolist()
    values = enc_year["Total Encounters"].tolist()

    echarts_annual_opts = {
        **ECHARTS_BASE,
        "legend": {"bottom": 5, "textStyle": {"color": "#1e293b"}},
        "toolbox": {
            "feature": {
                "saveAsImage": {},
                "dataView": {"readOnly": True},
                "restore": {},
                "magicType": {"type": ["line", "bar"]},
            }
        },
        "tooltip": {
            "trigger": "axis",
            "formatter": JsCode(
                "function(p){ return p[0].name + '<br/>Visits: ' + p[0].value.toLocaleString(); }"
            ).js_code,
        },
        "xAxis": {
            "type": "category",
            "data": years,
            "axisLabel": {"color": "#1e293b"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
        },
        "yAxis": {
            "type": "value",
            "axisLabel": {"color": "#1e293b"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
            "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
        },
        "dataZoom": [
            {"type": "inside", "start": 0, "end": 100},
            {"type": "slider", "start": 0, "end": 100, "height": 20, "bottom": 30},
        ],
        "grid": {"bottom": "18%"},
        "series": [
            {
                "name": "Total Encounters",
                "type": "bar",
                "data": values,
                "itemStyle": {"color": "#3b82f6"},
                "label": {"show": True, "position": "top", "color": "#1e293b"},
            }
        ],
    }
    st_echarts(options=echarts_annual_opts, height="400px", key="annual_visit_volume")

    st.subheader("Encounter Class Proportion per Year")
    st.caption("Distribution of encounter classes across years.")
    class_yr = (
        filtered_encounters.groupby(["YEAR", "ENCOUNTERCLASS"])
        .size()
        .reset_index(name="Total Encounters")
    )
    class_yr["Proportion (%)"] = class_yr.groupby("YEAR")["Total Encounters"].transform(
        lambda x: x / x.sum() * 100
    )
    class_yr.rename(
        columns={"YEAR": "Year", "ENCOUNTERCLASS": "Encounter Class"}, inplace=True
    )

    years = sorted(class_yr["Year"].unique())

    # Sort classes by total proportion (descending - largest first)
    class_totals = (
        class_yr.groupby("Encounter Class")["Total Encounters"]
        .sum()
        .sort_values(ascending=False)
    )
    classes = class_totals.index.tolist()

    series_data = []
    for i, enc_class in enumerate(classes):
        class_data = []
        for year in years:
            row = class_yr[
                (class_yr["Year"] == year) & (class_yr["Encounter Class"] == enc_class)
            ]
            val = row["Proportion (%)"].values[0] if len(row) > 0 else 0
            class_data.append(round(val, 1))
        series_data.append(
            {
                "name": enc_class,
                "type": "bar",
                "stack": "total",
                "data": class_data,
                "itemStyle": {"color": DISCRETE_COLORS[i % len(DISCRETE_COLORS)]},
                "emphasis": {"focus": "series"},
            }
        )

    echarts_class_opts = {
        **ECHARTS_BASE,
        "legend": {
            "bottom": 5,
            "textStyle": {"color": "#1e293b"},
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {},
                "dataView": {"readOnly": True},
                "restore": {},
            }
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "formatter": JsCode(
                "function(p){ let total = p.reduce((s, i) => s + i.value, 0); return p.map(i => i.seriesName + ': ' + i.value.toFixed(1) + '%').join('<br/>'); }"
            ).js_code,
        },
        "xAxis": {
            "type": "category",
            "data": [str(y) for y in years],
            "axisLabel": {"color": "#1e293b"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
        },
        "yAxis": {
            "type": "value",
            "axisLabel": {"color": "#1e293b", "formatter": "{value}%"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
            "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
        },
        "dataZoom": [
            {"type": "inside", "start": 0, "end": 100},
            {"type": "slider", "start": 0, "end": 100, "height": 20, "bottom": 30},
        ],
        "grid": {"bottom": "18%", "top": "8%"},
        "series": series_data,
    }
    st_echarts(
        options=echarts_class_opts, height="450px", key="encounter_class_proportion"
    )

    st.subheader("Encounter Duration Analysis")
    st.caption("Breakdown of encounters by duration (over/under 24 hours).")
    col1, col2 = st.columns([1, 1.5])
    with col1:
        dur_dist = filtered_encounters["IS_OVER_24H"].value_counts().reset_index()
        dur_dist["IS_OVER_24H"] = dur_dist["IS_OVER_24H"].map(
            {False: "Under 24 Hours", True: "Over 24 Hours"}
        )
        dur_dist.rename(
            columns={"IS_OVER_24H": "Duration Category", "count": "Total Encounters"},
            inplace=True,
        )
        fig3 = px.pie(
            dur_dist,
            names="Duration Category",
            values="Total Encounters",
            hole=0.65,
            template="plotly_white",
            color_discrete_sequence=["#00c9a7", "#ef4444"],
        )
        fig3.update_layout(showlegend=False)
        fig3.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=3)),
        )
        fig3 = style_plotly(fig3)
        st.plotly_chart(fig3, use_container_width=True, config=chart_config)
    st.divider()

    drill_col1, drill_col2 = st.columns(2)
    with drill_col1:
        st.markdown("**Over 24 Hours** :material/schedule:")
        over_24h = filtered_encounters[filtered_encounters["IS_OVER_24H"] == True]
        if not over_24h.empty:
            over_24h_class = over_24h["ENCOUNTERCLASS"].value_counts().reset_index()
            over_24h_class.columns = ["Encounter Class", "Count"]
            over_24h_class = over_24h_class.sort_values("Count", ascending=True)
            total_over = over_24h_class["Count"].sum()
            over_24h_class["Percentage"] = over_24h_class["Count"] / total_over * 100

            classes_over = over_24h_class["Encounter Class"].tolist()
            counts_over = over_24h_class["Count"].tolist()
            percentages_over = over_24h_class["Percentage"].tolist()

            echarts_over_opts = {
                **ECHARTS_BASE,
                "legend": {"bottom": 5, "textStyle": {"color": "#1e293b"}},
                "toolbox": {
                    "feature": {
                        "saveAsImage": {},
                        "dataView": {"readOnly": True},
                        "restore": {},
                        "magicType": {"type": ["line", "bar"]},
                    }
                },
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {"type": "shadow"},
                    "formatter": JsCode(
                        "function(p){ return p[0].name + '<br/>Count: ' + p[0].value.toLocaleString() + ' (' + p[0].value.toFixed ? '' : '' + ')'; }"
                    ).js_code,
                },
                "xAxis": {
                    "type": "value",
                    "axisLabel": {"color": "#1e293b"},
                    "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
                    "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
                },
                "yAxis": {
                    "type": "category",
                    "data": classes_over,
                    "axisLabel": {"color": "#1e293b"},
                    "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
                },
                "grid": {"left": "15%", "right": "10%", "bottom": "15%"},
                "series": [
                    {
                        "name": "Encounters",
                        "type": "bar",
                        "data": counts_over,
                        "itemStyle": {"color": "#ef4444"},
                        "label": {
                            "show": True,
                            "position": "right",
                            "color": "#1e293b",
                            "formatter": JsCode(
                                "function(p){ return p.value.toLocaleString(); }"
                            ).js_code,
                        },
                    }
                ],
            }
            st_echarts(
                options=echarts_over_opts, height="300px", key="over_24h_breakdown"
            )
        else:
            st.info("No encounters over 24 hours.")

    with drill_col2:
        st.markdown("**Under 24 Hours** :material/timer:")
        under_24h = filtered_encounters[filtered_encounters["IS_OVER_24H"] == False]
        if not under_24h.empty:
            under_24h_class = under_24h["ENCOUNTERCLASS"].value_counts().reset_index()
            under_24h_class.columns = ["Encounter Class", "Count"]
            under_24h_class = under_24h_class.sort_values("Count", ascending=True)
            total_under = under_24h_class["Count"].sum()
            under_24h_class["Percentage"] = under_24h_class["Count"] / total_under * 100

            classes_under = under_24h_class["Encounter Class"].tolist()
            counts_under = under_24h_class["Count"].tolist()

            echarts_under_opts = {
                **ECHARTS_BASE,
                "legend": {"bottom": 5, "textStyle": {"color": "#1e293b"}},
                "toolbox": {
                    "feature": {
                        "saveAsImage": {},
                        "dataView": {"readOnly": True},
                        "restore": {},
                        "magicType": {"type": ["line", "bar"]},
                    }
                },
                "tooltip": {
                    "trigger": "axis",
                    "axisPointer": {"type": "shadow"},
                },
                "xAxis": {
                    "type": "value",
                    "axisLabel": {"color": "#1e293b"},
                    "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
                    "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
                },
                "yAxis": {
                    "type": "category",
                    "data": classes_under,
                    "axisLabel": {"color": "#1e293b"},
                    "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
                },
                "grid": {"left": "15%", "right": "10%", "bottom": "15%"},
                "series": [
                    {
                        "name": "Encounters",
                        "type": "bar",
                        "data": counts_under,
                        "itemStyle": {"color": "#10b981"},
                        "label": {
                            "show": True,
                            "position": "right",
                            "color": "#1e293b",
                            "formatter": JsCode(
                                "function(p){ return p.value.toLocaleString(); }"
                            ).js_code,
                        },
                    }
                ],
            }
            st_echarts(
                options=echarts_under_opts, height="300px", key="under_24h_breakdown"
            )
        else:
            st.info("No encounters under 24 hours.")


# ----------------------------------------
# PAGE 3: COST & COVERAGE (SQL OBJECTIVE 2)
# ----------------------------------------
elif page == ":material/payments: Financials & Coverage":
    st.markdown("<h1>Financials & Procedures</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-subtitle'>Insurance coverage and procedure cost mapping.</div>",
        unsafe_allow_html=True,
    )

    zero_cov_count = (filtered_encounters["PAYER_COVERAGE"] == 0).sum()
    covered_count = len(filtered_encounters) - zero_cov_count
    total_coverage = filtered_encounters["PAYER_COVERAGE"].sum()
    total_cost = filtered_encounters["TOTAL_CLAIM_COST"].sum()
    overall_coverage_rate = (total_coverage / total_cost * 100) if total_cost > 0 else 0

    years_available = sorted(filtered_encounters["YEAR"].unique())
    if len(years_available) >= 2:
        current_year = years_available[-1]
        prev_year = years_available[-2]
        curr_enc = filtered_encounters[filtered_encounters["YEAR"] == current_year]
        prev_enc = filtered_encounters[filtered_encounters["YEAR"] == prev_year]

        curr_zero = (curr_enc["PAYER_COVERAGE"] == 0).sum()
        prev_zero = (prev_enc["PAYER_COVERAGE"] == 0).sum()
        delta_zero = calc_delta(curr_zero, prev_zero)

        curr_cov = curr_enc["PAYER_COVERAGE"].sum()
        prev_cov = prev_enc["PAYER_COVERAGE"].sum()
        curr_cost = curr_enc["TOTAL_CLAIM_COST"].sum()
        prev_cost = prev_enc["TOTAL_CLAIM_COST"].sum()
        curr_rate = (curr_cov / curr_cost * 100) if curr_cost > 0 else 0
        prev_rate = (prev_cov / prev_cost * 100) if prev_cost > 0 else 0
        delta_rate = calc_delta(curr_rate, prev_rate)

        delta_total_cov = calc_delta(curr_cov, prev_cov)
    else:
        delta_zero = delta_rate = delta_total_cov = None

    spark_zero = (
        [
            (
                filtered_encounters[filtered_encounters["YEAR"] == y]["PAYER_COVERAGE"]
                == 0
            ).sum()
            for y in years_available
        ]
        if len(years_available) > 1
        else None
    )

    spark_rate = []
    if len(years_available) > 1:
        for y in years_available:
            year_enc = filtered_encounters[filtered_encounters["YEAR"] == y]
            y_cov = year_enc["PAYER_COVERAGE"].sum()
            y_cost = year_enc["TOTAL_CLAIM_COST"].sum()
            rate = (y_cov / y_cost * 100) if y_cost > 0 else 0
            spark_rate.append(round(rate, 1))

    spark_total_cov = (
        [
            round(
                filtered_encounters[filtered_encounters["YEAR"] == y][
                    "PAYER_COVERAGE"
                ].sum()
                / 1_000_000,
                1,
            )
            for y in years_available
        ]
        if len(years_available) > 1
        else None
    )

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.metric(
            label="Zero Coverage Encounters",
            value=f"{zero_cov_count:,}",
            delta=delta_zero,
            border=True,
            chart_data=spark_zero if spark_zero and len(spark_zero) > 1 else None,
            chart_type="bar",
        )
    with kpi_col2:
        st.metric(
            label="Overall Coverage Rate",
            value=f"{overall_coverage_rate:.1f}%",
            delta=delta_rate,
            border=True,
            chart_data=spark_rate if spark_rate and len(spark_rate) > 1 else None,
            chart_type="line",
        )
    with kpi_col3:
        st.metric(
            label="Total Coverage Amount",
            value=f"${total_coverage:,.0f}",
            delta=delta_total_cov,
            border=True,
            chart_data=spark_total_cov
            if spark_total_cov and len(spark_total_cov) > 1
            else None,
            chart_type="area",
        )

    st.divider()

    st.subheader("Payer Summary")
    st.caption("Financial summary by insurance payer.")
    payer_summary = (
        filtered_encounters.groupby("PAYER_NAME")
        .agg(
            {
                "Id": "count",
                "TOTAL_CLAIM_COST": "sum",
                "PAYER_COVERAGE": "sum",
            }
        )
        .reset_index()
    )
    payer_summary.columns = ["Payer", "Encounters", "Total Cost", "Coverage"]
    payer_summary["Out of Pocket"] = (
        payer_summary["Total Cost"] - payer_summary["Coverage"]
    )
    payer_summary["Coverage Rate (%)"] = (
        payer_summary["Coverage"] / payer_summary["Total Cost"] * 100
    ).fillna(0)
    payer_summary["Coverage Rate (%)"] = payer_summary["Coverage Rate (%)"].round(1)
    payer_summary["Payer Type"] = (
        payer_summary["Payer"].map(PAYER_TYPE).fillna("Unknown")
    )
    payer_summary = payer_summary.sort_values("Encounters", ascending=False)

    display_df = payer_summary[
        [
            "Payer",
            "Payer Type",
            "Encounters",
            "Total Cost",
            "Coverage",
            "Out of Pocket",
            "Coverage Rate (%)",
        ]
    ].copy()

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total Cost": st.column_config.NumberColumn("Total Cost", format="$%,d"),
            "Coverage": st.column_config.NumberColumn("Coverage", format="$%,d"),
            "Out of Pocket": st.column_config.NumberColumn(
                "Out of Pocket", format="$%,d"
            ),
            "Encounters": st.column_config.NumberColumn("Encounters", format="%d"),
            "Coverage Rate (%)": st.column_config.NumberColumn(
                "Coverage Rate (%)", format="%.1f%%"
            ),
        },
    )

    st.divider()

    st.subheader("Coverage vs Out-of-Pocket by Payer")
    st.caption(
        "Comparing insurance coverage amount against patient out-of-pocket expenses."
    )
    payer_breakdown = payer_summary.sort_values("Total Cost", ascending=True)
    payers_break = payer_breakdown["Payer"].tolist()
    coverage_vals = [round(v, 2) for v in payer_breakdown["Coverage"].tolist()]
    oop_vals = [round(v, 2) for v in payer_breakdown["Out of Pocket"].tolist()]

    echarts_breakdown_opts = {
        **ECHARTS_BASE,
        "legend": {"bottom": 5, "textStyle": {"color": "#1e293b"}},
        "toolbox": {
            "feature": {
                "saveAsImage": {},
                "dataView": {"readOnly": True},
                "restore": {},
            }
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "formatter": JsCode(
                "function(p){ let total = p.reduce((s, i) => s + i.value, 0); return p[0].name + '<br/>' + p.map(i => i.seriesName + ': $' + i.value.toLocaleString()).join('<br/>') + '<br/>Total: $' + total.toLocaleString(); }"
            ).js_code,
        },
        "xAxis": {
            "type": "value",
            "axisLabel": {"color": "#1e293b", "formatter": "${value}"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
            "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
        },
        "yAxis": {
            "type": "category",
            "data": payers_break,
            "axisLabel": {"color": "#1e293b"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
        },
        "grid": {"left": "20%", "right": "10%", "bottom": "15%"},
        "series": [
            {
                "name": "Coverage",
                "type": "bar",
                "stack": "total",
                "data": coverage_vals,
                "itemStyle": {"color": "#10b981"},
                "emphasis": {"focus": "series"},
            },
            {
                "name": "Out of Pocket",
                "type": "bar",
                "stack": "total",
                "data": oop_vals,
                "itemStyle": {"color": "#ef4444"},
                "emphasis": {"focus": "series"},
            },
        ],
    }
    st_echarts(options=echarts_breakdown_opts, height="400px", key="coverage_vs_oop")

    st.divider()

    st.subheader("Medical Procedures Mapping")
    st.caption("Procedure frequency and average cost analysis.")
    if not filtered_procedures.empty:
        proc_stats = (
            filtered_procedures.groupby("DESCRIPTION")
            .agg(
                Times_Performed=("DESCRIPTION", "size"),
                Avg_Base_Cost=("BASE_COST", "mean"),
            )
            .reset_index()
        )
        proc_stats.rename(
            columns={
                "DESCRIPTION": "Procedure",
                "Times_Performed": "Count",
                "Avg_Base_Cost": "Avg Cost ($)",
            },
            inplace=True,
        )
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Top 10 Frequency**")
            st.dataframe(
                proc_stats.nlargest(10, "Count").style.format(
                    {"Avg Cost ($)": "${:,.2f}"}
                ),
                use_container_width=True,
                hide_index=True,
            )
        with col_b:
            st.markdown("**Top 10 High Cost**")
            st.dataframe(
                proc_stats.nlargest(10, "Avg Cost ($)").style.format(
                    {"Avg Cost ($)": "${:,.2f}"}
                ),
                use_container_width=True,
                hide_index=True,
            )


# ----------------------------------------
# PAGE 4: PATIENT BEHAVIOR (SQL OBJECTIVE 3)
# ----------------------------------------
elif page == ":material/groups: Patient Behavior":
    st.markdown("<h1>Patient Behavior Analytics</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-subtitle'>Tracking unique patients and readmission trends.</div>",
        unsafe_allow_html=True,
    )

    total_readmissions = filtered_encounters["IS_READMIT_30D"].sum()
    readmission_rate = (
        (total_readmissions / total_encounters * 100) if total_encounters > 0 else 0
    )

    years_available = sorted(filtered_encounters["YEAR"].unique())
    if len(years_available) >= 2:
        current_year = years_available[-1]
        prev_year = years_available[-2]
        curr_enc = filtered_encounters[filtered_encounters["YEAR"] == current_year]
        prev_enc = filtered_encounters[filtered_encounters["YEAR"] == prev_year]

        curr_readmit = curr_enc["IS_READMIT_30D"].sum()
        prev_readmit = prev_enc["IS_READMIT_30D"].sum()
        delta_readmit = calc_delta(curr_readmit, prev_readmit)

        curr_total = len(curr_enc)
        prev_total = len(prev_enc)
        curr_rate = (curr_readmit / curr_total * 100) if curr_total > 0 else 0
        prev_rate = (prev_readmit / prev_total * 100) if prev_total > 0 else 0
        delta_rate = calc_delta(curr_rate, prev_rate)

        curr_patients = curr_enc[curr_enc["IS_READMIT_30D"]]["PATIENT"].nunique()
        prev_patients = prev_enc[prev_enc["IS_READMIT_30D"]]["PATIENT"].nunique()
        delta_patients = calc_delta(curr_patients, prev_patients)
    else:
        delta_readmit = delta_rate = delta_patients = None

    spark_readmit = (
        [
            filtered_encounters[filtered_encounters["YEAR"] == y][
                "IS_READMIT_30D"
            ].sum()
            for y in years_available
        ]
        if len(years_available) > 1
        else None
    )

    spark_rate = []
    if len(years_available) > 1:
        for y in years_available:
            year_enc = filtered_encounters[filtered_encounters["YEAR"] == y]
            y_readmit = year_enc["IS_READMIT_30D"].sum()
            y_total = len(year_enc)
            rate = (y_readmit / y_total * 100) if y_total > 0 else 0
            spark_rate.append(round(rate, 1))

    spark_patients = (
        [
            filtered_encounters[
                (filtered_encounters["YEAR"] == y)
                & (filtered_encounters["IS_READMIT_30D"])
            ]["PATIENT"].nunique()
            for y in years_available
        ]
        if len(years_available) > 1
        else None
    )

    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.metric(
            label="Total Readmissions (30-day)",
            value=f"{total_readmissions:,}",
            delta=delta_readmit,
            border=True,
            chart_data=spark_readmit
            if spark_readmit and len(spark_readmit) > 1
            else None,
            chart_type="bar",
        )
    with kpi_col2:
        st.metric(
            label="Readmission Rate",
            value=f"{readmission_rate:.1f}%",
            delta=delta_rate,
            border=True,
            chart_data=spark_rate if spark_rate and len(spark_rate) > 1 else None,
            chart_type="line",
        )
    with kpi_col3:
        st.metric(
            label="Unique Patients Readmitted",
            value=f"{readmitted_patients_count:,}",
            delta=delta_patients,
            border=True,
            chart_data=spark_patients
            if spark_patients and len(spark_patients) > 1
            else None,
            chart_type="area",
        )

    st.subheader("Unique Patients per Quarter")
    st.caption("Distinct patient count per quarter period.")
    pat_qtr = (
        filtered_encounters.groupby("QUARTER")["PATIENT"]
        .nunique()
        .reset_index(name="Unique Patients")
    )
    pat_qtr.rename(columns={"QUARTER": "Quarter"}, inplace=True)

    quarters = pat_qtr["Quarter"].tolist()
    patient_counts = pat_qtr["Unique Patients"].tolist()

    echarts_pat_qtr_opts = {
        **ECHARTS_BASE,
        "legend": {"bottom": 5, "textStyle": {"color": "#1e293b"}},
        "toolbox": {
            "feature": {
                "saveAsImage": {},
                "dataView": {"readOnly": True},
                "restore": {},
                "magicType": {"type": ["line", "bar"]},
            }
        },
        "tooltip": {
            "trigger": "axis",
            "formatter": JsCode(
                "function(p){ return p[0].name + '<br/>Unique Patients: ' + p[0].value.toLocaleString(); }"
            ).js_code,
        },
        "xAxis": {
            "type": "category",
            "data": quarters,
            "axisLabel": {"color": "#1e293b"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
        },
        "yAxis": {
            "type": "value",
            "axisLabel": {"color": "#1e293b"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
            "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
        },
        "dataZoom": [
            {"type": "inside", "start": 0, "end": 100},
            {"type": "slider", "start": 0, "end": 100, "height": 20, "bottom": 30},
        ],
        "grid": {"bottom": "18%", "top": "8%"},
        "series": [
            {
                "name": "Unique Patients",
                "type": "line",
                "data": patient_counts,
                "smooth": True,
                "symbol": "circle",
                "symbolSize": 8,
                "lineStyle": {"color": "#10b981", "width": 3},
                "itemStyle": {
                    "color": "#10b981",
                    "borderColor": "#ffffff",
                    "borderWidth": 2,
                },
                "areaStyle": {"color": "#10b981", "opacity": 0.2},
            }
        ],
    }
    st_echarts(
        options=echarts_pat_qtr_opts, height="400px", key="unique_patients_per_quarter"
    )

    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.subheader("Readmission Ratio")
        st.caption("Proportion of patients readmitted within 30 days.")
        readmit_df = pd.DataFrame(
            {
                "Status": ["Readmitted", "Not Readmitted"],
                "Patients": [
                    readmitted_patients_count,
                    unique_patients - readmitted_patients_count,
                ],
            }
        )
        fig_readmit = px.pie(
            readmit_df,
            names="Status",
            values="Patients",
            hole=0.65,
            template="plotly_white",
            color_discrete_sequence=["#ef4444", "#3b82f6"],
        )
        fig_readmit.update_layout(showlegend=False)
        fig_readmit.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=3)),
        )
        fig_readmit = style_plotly(fig_readmit)
        st.plotly_chart(fig_readmit, use_container_width=True, config=chart_config)

    with col2:
        st.subheader("Top Readmitted Patients")
        st.caption("Patients with the highest readmission frequency.")
        readmit_counts = (
            filtered_encounters[filtered_encounters["IS_READMIT_30D"]]
            .groupby("PATIENT")
            .size()
            .reset_index(name="Readmissions")
        )
        if not readmit_counts.empty:
            top_patients = readmit_counts.merge(
                patients[["Id", "FIRST", "LAST"]], left_on="PATIENT", right_on="Id"
            )
            top_patients["Name"] = top_patients["FIRST"] + " " + top_patients["LAST"]
            st.dataframe(
                top_patients[["Name", "Readmissions"]]
                .nlargest(10, "Readmissions")
                .style.background_gradient(cmap="Reds"),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No readmissions found.")

    st.divider()

    st.subheader("Readmissions by Encounter Class")
    st.caption("Distribution of 30-day readmissions by encounter type.")
    readmit_by_class = (
        filtered_encounters[filtered_encounters["IS_READMIT_30D"]]
        .groupby("ENCOUNTERCLASS")
        .size()
        .reset_index(name="Readmissions")
    )
    readmit_by_class = readmit_by_class.sort_values("Readmissions", ascending=True)

    classes_readmit = readmit_by_class["ENCOUNTERCLASS"].tolist()
    counts_readmit = readmit_by_class["Readmissions"].tolist()

    echarts_readmit_class_opts = {
        **ECHARTS_BASE,
        "legend": {"bottom": 5, "textStyle": {"color": "#1e293b"}},
        "toolbox": {
            "feature": {
                "saveAsImage": {},
                "dataView": {"readOnly": True},
                "restore": {},
                "magicType": {"type": ["line", "bar"]},
            }
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "formatter": JsCode(
                "function(p){ return p[0].name + '<br/>Readmissions: ' + p[0].value.toLocaleString(); }"
            ).js_code,
        },
        "xAxis": {
            "type": "value",
            "axisLabel": {"color": "#1e293b"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
            "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
        },
        "yAxis": {
            "type": "category",
            "data": classes_readmit,
            "axisLabel": {"color": "#1e293b"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
        },
        "grid": {"left": "15%", "right": "12%", "bottom": "15%"},
        "series": [
            {
                "name": "Readmissions",
                "type": "bar",
                "data": counts_readmit,
                "itemStyle": {"color": "#ef4444"},
                "label": {
                    "show": True,
                    "position": "right",
                    "color": "#1e293b",
                    "formatter": JsCode(
                        "function(p){ return p.value.toLocaleString(); }"
                    ).js_code,
                },
            }
        ],
    }
    st_echarts(
        options=echarts_readmit_class_opts, height="400px", key="readmissions_by_class"
    )

    st.subheader("Readmissions by Payer (Insurance)")
    st.caption("Distribution of 30-day readmissions by insurance provider.")
    readmit_by_payer = (
        filtered_encounters[filtered_encounters["IS_READMIT_30D"]]
        .groupby("PAYER_NAME")
        .size()
        .reset_index(name="Readmissions")
    )
    readmit_by_payer = readmit_by_payer.sort_values("Readmissions", ascending=True)

    payers_readmit = readmit_by_payer["PAYER_NAME"].tolist()
    counts_payer = readmit_by_payer["Readmissions"].tolist()

    echarts_readmit_payer_opts = {
        **ECHARTS_BASE,
        "legend": {"bottom": 5, "textStyle": {"color": "#1e293b"}},
        "toolbox": {
            "feature": {
                "saveAsImage": {},
                "dataView": {"readOnly": True},
                "restore": {},
                "magicType": {"type": ["line", "bar"]},
            }
        },
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {"type": "shadow"},
            "formatter": JsCode(
                "function(p){ return p[0].name + '<br/>Readmissions: ' + p[0].value.toLocaleString(); }"
            ).js_code,
        },
        "xAxis": {
            "type": "value",
            "axisLabel": {"color": "#1e293b"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
            "splitLine": {"lineStyle": {"color": "#e2e8f0"}},
        },
        "yAxis": {
            "type": "category",
            "data": payers_readmit,
            "axisLabel": {"color": "#1e293b"},
            "axisLine": {"lineStyle": {"color": "#cbd5e1"}},
        },
        "grid": {"left": "20%", "right": "12%", "bottom": "15%"},
        "series": [
            {
                "name": "Readmissions",
                "type": "bar",
                "data": counts_payer,
                "itemStyle": {"color": "#f59e0b"},
                "label": {
                    "show": True,
                    "position": "right",
                    "color": "#1e293b",
                    "formatter": JsCode(
                        "function(p){ return p.value.toLocaleString(); }"
                    ).js_code,
                },
            }
        ],
    }
    st_echarts(
        options=echarts_readmit_payer_opts, height="400px", key="readmissions_by_payer"
    )
