import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="RevOps Dashboard", layout="wide")

st.title("📊 AI-Powered RevOps Dashboard")
st.markdown("This dashboard simulates key RevOps insights using AI-generated data.")

# Load data
leads = pd.read_csv("data/leads.csv")
opps = pd.read_csv("data/opportunities.csv")

# Data prep
opps["weighted_amount"] = opps["amount"] * (opps["probability"] / 100)
opps["created_date"] = pd.to_datetime(opps["created_date"], errors="coerce")

# Metrics at a glance
st.markdown("### 🚀 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Pipeline", f"${opps['amount'].sum():,.0f}")
col2.metric("Avg Lead Score", f"{leads['lead_score'].mean():.1f}")
col3.metric("Lead → Opp Conversion", f"{leads['converted_to_opportunity'].mean()*100:.1f}%")
st.markdown("---")

# Funnel Overview
st.subheader("🔁 Funnel Overview")
col4, col5 = st.columns(2)
col4.bar_chart(leads["status"].value_counts())
col5.bar_chart(leads["source"].value_counts())

# Rep Performance
st.subheader("👤 Rep Pipeline Totals")
pipeline_by_rep = opps.groupby("assigned_rep")["amount"].sum().reset_index()
pipeline_by_rep.columns = ["Rep", "Total Pipeline ($)"]
pipeline_by_rep["Total Pipeline ($)"] = pd.to_numeric(pipeline_by_rep["Total Pipeline ($)"], errors="coerce")
bar = alt.Chart(pipeline_by_rep).mark_bar().encode(
    x=alt.X("Rep:N", title="Sales Rep"),
    y=alt.Y("Total Pipeline ($):Q", title="Pipeline ($)")
).properties(title="Pipeline by Rep")
st.altair_chart(bar, use_container_width=True)

# Stage distribution
st.subheader("📊 Opportunity Stage Breakdown")
st.bar_chart(opps["stage"].value_counts())

# Forecast
st.subheader("📈 Weighted Forecast by Stage")
forecast = opps.groupby("stage")["weighted_amount"].sum().reset_index()
forecast.columns = ["Stage", "Weighted Pipeline ($)"]
st.dataframe(forecast)

# Strategic Insights
st.markdown("---")
st.header("🧠 Strategic Insights")
top_rep_weighted = opps.groupby("assigned_rep")["weighted_amount"].sum().idxmax()
top_rep_total = opps.groupby("assigned_rep")["amount"].sum().idxmax()
top_source = leads["source"].value_counts().idxmax()
converted = leads[leads["converted_to_opportunity"] == True]
conversion_by_source = (
    converted["source"].value_counts() / leads["source"].value_counts()
).dropna()
top_conversion_source = conversion_by_source.idxmax()
longest_stage = (
    opps.groupby("stage")["days_in_stage"].mean().sort_values(ascending=False).idxmax()
)
recent_opps = opps[opps["created_date"] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
recent_avg = recent_opps["amount"].mean()

st.markdown(f"**🏆 Top Performer:** {top_rep_total} leads in total and forecast-weighted pipeline.")
st.markdown(f"**🌱 Most Common Lead Source:** {top_source}")
st.markdown(f"**🎯 Best-Converting Source:** {top_conversion_source} — highest opportunity conversion.")
st.markdown(f"**🐢 Longest Stage Delay:** {longest_stage} takes the longest on average.")
if pd.isna(recent_avg):
    st.warning("📉 No new opportunities created in the past 30 days.")
else:
    st.markdown(f"**📈 Recent Avg Pipeline Value:** ${recent_avg:,.0f}")
