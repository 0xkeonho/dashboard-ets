import streamlit as st
import pandas as pd
from utils import (
    load_data,
    render_sidebar_filters,
    apply_filters,
    get_sparkline_data,
    calc_delta,
    ECHARTS_BASE,
    DISCRETE_COLORS,
    CHART_CONFIG,
    style_plotly,
)
from streamlit_echarts import st_echarts, JsCode

st.set_page_config(
    page_title="Dashboard Overview - MGH Analytics",
    page_icon=":material/dashboard:",
    layout="wide",
)

encounters, patients, payers, procedures, missing_files = load_data()

if missing_files:
    st.error(f"CSV files not found: {', '.join(missing_files)}")
    st.stop()

selected_years, selected_payers, selected_classes = render_sidebar_filters(encounters)
filtered_encounters, filtered_procedures = apply_filters(
    encounters, procedures, selected_years, selected_payers, selected_classes
)

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
        last_12_months.groupby("YEAR_MONTH").size().reset_index(name="Total Encounters")
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
