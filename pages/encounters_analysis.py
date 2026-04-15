import streamlit as st
import pandas as pd
import plotly.express as px
from utils import (
    apply_filters,
    ECHARTS_BASE,
    DISCRETE_COLORS,
    CHART_CONFIG,
    style_plotly,
)
from streamlit_echarts import st_echarts, JsCode

encounters = st.session_state.get("encounters")
procedures = st.session_state.get("procedures")
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
st_echarts(options=echarts_class_opts, height="450px", key="encounter_class_proportion")

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
    st.plotly_chart(fig3, use_container_width=True, config=CHART_CONFIG)
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
        st_echarts(options=echarts_over_opts, height="300px", key="over_24h_breakdown")
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

st.divider()

st.subheader("Key Insights")
st.markdown(
    """
- **Ambulatory mendominasi (45%)** — MGH adalah rumah sakit dengan fokus rawat jalan, bukan rawat inap.
- **Peak hour jam 02:00** — Tingginya kunjungan di malam hari, kemungkinan besar untuk kasus emergency/urgent care.
- **Trend kunjungan naik** — Pertumbuhan dari 2011-2014, stabil 2015-2020, dan lonjakan di 2021.
"""
)

st.subheader("Recommendations")
st.markdown(
    """
- **Evaluasi kapasitas ambulatory** — 45% beban di ambulatory, perlu dipastikan kapasitas cukup saat jam sibuk (pagi-siang).
- **Optimasi staffing malam** — Peak hour jam 02:00 membutuhkan staff lebih banyak untuk handle urgent/emergency.
"""
)
