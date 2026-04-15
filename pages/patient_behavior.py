import streamlit as st
import pandas as pd
import plotly.express as px
from utils import (
    apply_filters,
    calc_delta,
    ECHARTS_BASE,
    CHART_CONFIG,
    style_plotly,
)
from streamlit_echarts import st_echarts, JsCode

encounters = st.session_state.get("encounters")
procedures = st.session_state.get("procedures")
patients = st.session_state.get("patients")
selected_years = st.session_state.get("selected_years")
selected_payers = st.session_state.get("selected_payers")
selected_classes = st.session_state.get("selected_classes")

if encounters is None or encounters.empty:
    st.warning("No data available.")
    st.stop()

filtered_encounters, filtered_procedures = apply_filters(
    encounters, procedures, selected_years, selected_payers, selected_classes
)

if filtered_encounters.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

total_encounters = len(filtered_encounters)
unique_patients = (
    filtered_encounters["PATIENT"].nunique() if not filtered_encounters.empty else 0
)
readmitted_patients_count = (
    filtered_encounters[filtered_encounters["IS_READMIT_30D"]]["PATIENT"].nunique()
    if not filtered_encounters.empty
    else 0
)

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
        filtered_encounters[filtered_encounters["YEAR"] == y]["IS_READMIT_30D"].sum()
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
            (filtered_encounters["YEAR"] == y) & (filtered_encounters["IS_READMIT_30D"])
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
        chart_data=spark_readmit if spark_readmit and len(spark_readmit) > 1 else None,
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
    st.plotly_chart(fig_readmit, use_container_width=True, config=CHART_CONFIG)

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

st.divider()

st.subheader("Key Insights")
st.markdown(
    """
- **Readmission rate 60.2% SANGAT TINGGI** — Industry benchmark untuk 30-day readmission adalah 15-20%. MGH memiliki 3x lipat dari normal.
- **Chronic conditions driver utama** — Heart failure dan hyperlipidemia adalah penyakit kronis yang butuh long-term management.
- **Super-utilizers** — 9 pasien (1%) = 19.6% dari total encounters, menunjukkan small group yang memakan resource besar.
- **NO_INSURANCE & Medicare readmission tinggi** — Populasi vulnerable tanpa atau dengan limited coverage cenderung readmit lebih sering.
"""
)

st.subheader("Recommendations")
st.markdown(
    """
- **Care Transitions Program** — 60% readmission mengindikasikan issue discharge planning. Perlu follow-up post-discharge.
- **Disease Management Program untuk chronic conditions** — Heart failure adalah top diagnosis. Program self-management education bisa kurangi readmission.
- **Case Management untuk super-utilizers** — 9 pasien = 20% encounters. Intervention targeted untuk mereka akan berdampak besar.
- **Target NO_INSURANCE & Medicare population** — Mereka readmit paling banyak. Perlu social work + community resources integration.
"""
)
