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
            "title": {
                "text": "Last 12 Months Encounters",
                "left": "center",
                "top": 5,
            },
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
            "xAxis": {"type": "category", "data": months, "axisLabel": {"rotate": 45}},
            "yAxis": {"type": "value"},
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
                    "areaStyle": {"opacity": 0.3},
                    "label": {"show": True, "position": "top"},
                }
            ],
        }
        st_echarts(
            options=echarts_monthly_opts, height="400px", key="monthly_encounter_trend"
        )

    with col2:
        st.subheader("Encounter Class Distribution")
        class_dist = filtered_encounters["ENCOUNTERCLASS"].value_counts().reset_index()
        class_dist.columns = ["Encounter Class", "Total Encounters"]
        fig2 = px.pie(
            class_dist,
            names="Encounter Class",
            values="Total Encounters",
            hole=0.65,
            template="plotly_white",
            color_discrete_sequence=DISCRETE_COLORS,
        )
        fig2.update_layout(
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center")
        )
        fig2.update_traces(marker=dict(line=dict(color="#ffffff", width=3)))
        fig2 = style_plotly(fig2)
        st.plotly_chart(fig2, use_container_width=True, config=chart_config)


# ----------------------------------------
# PAGE 2: ENCOUNTERS (SQL OBJECTIVE 1)
# ----------------------------------------
elif page == ":material/swap_horiz: Encounters Analysis":
    st.markdown("<h1>Encounters & Visits</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-subtitle'>Volume trends, service proportions, and durations.<br/><em>SQL Objective 1: Encounters Overview</em></div>",
        unsafe_allow_html=True,
    )

    st.subheader("Annual Visit Volume")
    enc_year = (
        filtered_encounters.groupby("YEAR").size().reset_index(name="Total Encounters")
    )
    enc_year.rename(columns={"YEAR": "Year"}, inplace=True)

    years = enc_year["Year"].astype(str).tolist()
    values = enc_year["Total Encounters"].tolist()

    echarts_annual_opts = {
        "title": {"text": "Annual Visit Volume", "left": "center", "top": 5},
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
        "xAxis": {"type": "category", "data": years},
        "yAxis": {"type": "value"},
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
                "label": {"show": True, "position": "top"},
            }
        ],
    }
    st_echarts(options=echarts_annual_opts, height="400px", key="annual_visit_volume")

    st.subheader("Encounter Class Proportion per Year")
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
    fig2 = px.bar(
        class_yr,
        x="Year",
        y="Proportion (%)",
        color="Encounter Class",
        template="plotly_white",
        barmode="stack",
        color_discrete_sequence=DISCRETE_COLORS,
    )
    fig2.update_layout(legend=dict(orientation="h", y=-0.2, title=None))
    fig2 = style_plotly(fig2)
    st.plotly_chart(fig2, use_container_width=True, config=chart_config)

    st.subheader("Encounter Duration Analysis")
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
    with col2:
        st.markdown(
            '<div class="insight-box">Treatments exceeding the 24-hour mark are almost exclusively dominated by Inpatient and Emergency cases.</div>',
            unsafe_allow_html=True,
        )


# ----------------------------------------
# PAGE 3: COST & COVERAGE (SQL OBJECTIVE 2)
# ----------------------------------------
elif page == ":material/payments: Financials & Coverage":
    st.markdown("<h1>Financials & Procedures</h1>", unsafe_allow_html=True)
    st.markdown(
        "<div class='page-subtitle'>Insurance coverage and procedure cost mapping.<br/><em>SQL Objective 2: Cost & Coverage Insights</em></div>",
        unsafe_allow_html=True,
    )

    zero_cov_count = (filtered_encounters["PAYER_COVERAGE"] == 0).sum()
    covered_count = len(filtered_encounters) - zero_cov_count
    total_coverage = filtered_encounters["PAYER_COVERAGE"].sum()
    total_cost = filtered_encounters["TOTAL_CLAIM_COST"].sum()
    overall_coverage_rate = (total_coverage / total_cost * 100) if total_cost > 0 else 0

    coverage_kpis = f"""
    <div class="kpi-container">
        <div class="kpi-card"><div class="kpi-title">Zero Coverage Encounters</div><div class="kpi-value val-red">{zero_cov_count:,}</div></div>
        <div class="kpi-card"><div class="kpi-title">Overall Coverage Rate</div><div class="kpi-value val-green">{overall_coverage_rate:.1f}%</div></div>
        <div class="kpi-card"><div class="kpi-title">Total Coverage Amount</div><div class="kpi-value val-blue">${total_coverage:,.0f}</div></div>
    </div>
    """
    st.markdown(coverage_kpis, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Coverage Proportion")
        cov_df = pd.DataFrame(
            {
                "Status": ["Covered", "No Insurance"],
                "Count": [covered_count, zero_cov_count],
            }
        )
        fig_cov = px.pie(
            cov_df,
            names="Status",
            values="Count",
            hole=0.65,
            template="plotly_white",
            color_discrete_sequence=["#10b981", "#ef4444"],
        )
        fig_cov.update_layout(showlegend=False)
        fig_cov.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=3)),
        )
        fig_cov = style_plotly(fig_cov)
        st.plotly_chart(fig_cov, use_container_width=True, config=chart_config)

    with c2:
        st.subheader("Avg Total Claim Cost by Payer")
        payer_cost = (
            filtered_encounters.groupby("PAYER_NAME")["TOTAL_CLAIM_COST"]
            .mean()
            .reset_index()
        )
        payer_cost.rename(
            columns={"PAYER_NAME": "Payer", "TOTAL_CLAIM_COST": "Avg Cost"},
            inplace=True,
        )
        payer_cost = payer_cost.sort_values("Avg Cost", ascending=True)
        payer_cost["Label"] = payer_cost["Avg Cost"].apply(lambda x: f"${x:,.0f}")
        fig_payer = px.bar(
            payer_cost,
            x="Avg Cost",
            y="Payer",
            orientation="h",
            template="plotly_white",
            color_discrete_sequence=["#f59e0b"],
            text="Label",
        )
        fig_payer.update_traces(textposition="outside")
        fig_payer = style_plotly(fig_payer)
        st.plotly_chart(fig_payer, use_container_width=True, config=chart_config)

    st.divider()

    st.subheader("Coverage Rate by Payer")
    payer_coverage = (
        filtered_encounters.groupby("PAYER_NAME")
        .agg({"TOTAL_CLAIM_COST": "sum", "PAYER_COVERAGE": "sum"})
        .reset_index()
    )
    payer_coverage["Coverage Rate (%)"] = (
        payer_coverage["PAYER_COVERAGE"] / payer_coverage["TOTAL_CLAIM_COST"] * 100
    ).fillna(0)
    payer_coverage["Coverage Rate (%)"] = payer_coverage["Coverage Rate (%)"].round(1)
    payer_coverage = payer_coverage.sort_values("Coverage Rate (%)", ascending=True)
    payer_coverage["Label"] = payer_coverage["Coverage Rate (%)"].apply(
        lambda x: f"{x:.1f}%"
    )

    fig_cov_rate = px.bar(
        payer_coverage,
        x="Coverage Rate (%)",
        y="PAYER_NAME",
        orientation="h",
        template="plotly_white",
        color_discrete_sequence=["#10b981"],
        text="Label",
        range_x=[0, 100],
    )
    fig_cov_rate.add_vline(
        x=50, line_dash="dash", line_color="#6b8099", annotation_text="50%"
    )
    fig_cov_rate.update_traces(textposition="outside")
    fig_cov_rate = style_plotly(fig_cov_rate)
    st.plotly_chart(fig_cov_rate, use_container_width=True, config=chart_config)

    st.subheader("Coverage vs Out-of-Pocket by Payer")
    payer_breakdown = (
        filtered_encounters.groupby("PAYER_NAME")
        .agg({"PAYER_COVERAGE": "sum", "TOTAL_CLAIM_COST": "sum"})
        .reset_index()
    )
    payer_breakdown["Out of Pocket"] = (
        payer_breakdown["TOTAL_CLAIM_COST"] - payer_breakdown["PAYER_COVERAGE"]
    )
    payer_breakdown = payer_breakdown.sort_values("TOTAL_CLAIM_COST", ascending=True)

    fig_breakdown = px.bar(
        payer_breakdown,
        y="PAYER_NAME",
        x=["PAYER_COVERAGE", "Out of Pocket"],
        orientation="h",
        template="plotly_white",
        color_discrete_map={"PAYER_COVERAGE": "#10b981", "Out of Pocket": "#ef4444"},
        labels={
            "PAYER_COVERAGE": "Coverage ($)",
            "Out of Pocket": "Out-of-Pocket ($)",
            "PAYER_NAME": "Payer",
        },
    )
    fig_breakdown.update_layout(
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center")
    )
    fig_breakdown = style_plotly(fig_breakdown)
    st.plotly_chart(fig_breakdown, use_container_width=True, config=chart_config)

    st.divider()

    st.subheader("Medical Procedures Mapping")
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
        "<div class='page-subtitle'>Tracking unique patients and readmission trends.<br/><em>SQL Objective 3: Patient Behavior Analysis</em></div>",
        unsafe_allow_html=True,
    )

    total_readmissions = filtered_encounters["IS_READMIT_30D"].sum()
    readmission_rate = (
        (total_readmissions / total_encounters * 100) if total_encounters > 0 else 0
    )

    readmission_kpis = f"""
    <div class="kpi-container">
        <div class="kpi-card"><div class="kpi-title">Total Readmissions (30-day)</div><div class="kpi-value val-red">{total_readmissions:,}</div></div>
        <div class="kpi-card"><div class="kpi-title">Readmission Rate</div><div class="kpi-value val-red">{readmission_rate:.1f}%</div></div>
        <div class="kpi-card"><div class="kpi-title">Unique Patients Readmitted</div><div class="kpi-value val-amber">{readmitted_patients_count:,}</div></div>
    </div>
    """
    st.markdown(readmission_kpis, unsafe_allow_html=True)

    st.subheader("Unique Patients per Quarter")
    pat_qtr = (
        filtered_encounters.groupby("QUARTER")["PATIENT"]
        .nunique()
        .reset_index(name="Unique Patients")
    )
    pat_qtr.rename(columns={"QUARTER": "Quarter"}, inplace=True)
    fig_qtr = px.line(
        pat_qtr,
        x="Quarter",
        y="Unique Patients",
        markers=True,
        template="plotly_white",
        color_discrete_sequence=["#00c9a7"],
    )
    fig_qtr.update_traces(
        fill="tozeroy",
        line=dict(width=3),
        marker=dict(size=8, color="#10b981", line=dict(width=2, color="#ffffff")),
    )
    fig_qtr = style_plotly(fig_qtr, add_zoom=True)
    st.plotly_chart(fig_qtr, use_container_width=True, config=chart_config_zoom)

    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.subheader("Readmission Ratio")
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
    readmit_by_class = (
        filtered_encounters[filtered_encounters["IS_READMIT_30D"]]
        .groupby("ENCOUNTERCLASS")
        .size()
        .reset_index(name="Readmissions")
    )
    readmit_by_class = readmit_by_class.sort_values("Readmissions", ascending=True)
    readmit_by_class["Label"] = readmit_by_class["Readmissions"].apply(
        lambda x: f"{x:,}"
    )

    fig_readmit_class = px.bar(
        readmit_by_class,
        x="Readmissions",
        y="ENCOUNTERCLASS",
        orientation="h",
        template="plotly_white",
        color_discrete_sequence=["#ef4444"],
        text="Label",
    )
    fig_readmit_class.update_traces(textposition="outside")
    fig_readmit_class = style_plotly(fig_readmit_class)
    st.plotly_chart(fig_readmit_class, use_container_width=True, config=chart_config)

    st.subheader("Readmissions by Payer (Insurance)")
    readmit_by_payer = (
        filtered_encounters[filtered_encounters["IS_READMIT_30D"]]
        .groupby("PAYER_NAME")
        .size()
        .reset_index(name="Readmissions")
    )
    readmit_by_payer = readmit_by_payer.sort_values("Readmissions", ascending=True)
    readmit_by_payer["Label"] = readmit_by_payer["Readmissions"].apply(
        lambda x: f"{x:,}"
    )

    fig_readmit_payer = px.bar(
        readmit_by_payer,
        x="Readmissions",
        y="PAYER_NAME",
        orientation="h",
        template="plotly_white",
        color_discrete_sequence=["#f59e0b"],
        text="Label",
    )
    fig_readmit_payer.update_traces(textposition="outside")
    fig_readmit_payer = style_plotly(fig_readmit_payer)
    st.plotly_chart(fig_readmit_payer, use_container_width=True, config=chart_config)
