import streamlit as st
from utils import (
    apply_filters,
    calc_delta,
    ECHARTS_BASE,
    PAYER_TYPE,
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
            filtered_encounters[filtered_encounters["YEAR"] == y]["PAYER_COVERAGE"] == 0
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
payer_summary["Out of Pocket"] = payer_summary["Total Cost"] - payer_summary["Coverage"]
payer_summary["Coverage Rate (%)"] = (
    payer_summary["Coverage"] / payer_summary["Total Cost"] * 100
).fillna(0)
payer_summary["Coverage Rate (%)"] = payer_summary["Coverage Rate (%)"].round(1)
payer_summary["Payer Type"] = payer_summary["Payer"].map(PAYER_TYPE).fillna("Unknown")
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
        "Out of Pocket": st.column_config.NumberColumn("Out of Pocket", format="$%,d"),
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
            proc_stats.nlargest(10, "Count").style.format({"Avg Cost ($)": "${:,.2f}"}),
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
