import streamlit as st
import pandas as pd

st.set_page_config(page_title="RevOps Dashboard", layout="wide")

st.title("AI-Powered RevOps Dashboard")
st.write("This dashboard uses AI-generated mock data to simulate core RevOps metrics.")

# Load data
leads = pd.read_csv("data/leads.csv")
opps = pd.read_csv("data/opportunities.csv")

# -------------------------------
# Funnel Overview
# -------------------------------
st.header("🔁 Funnel Overview")
st.subheader("Lead Status Distribution")
st.bar_chart(leads["status"].value_counts())

st.subheader("Leads by Source")
st.bar_chart(leads["source"].value_counts())

# -------------------------------
# Rep Performance
# -------------------------------
st.header("👤 Rep Performance")
pipeline_by_rep = opps.groupby("assigned_rep")["amount"].sum().reset_index()
pipeline_by_rep.columns = ["Rep", "Total Pipeline ($)"]
pipeline_by_rep["Total Pipeline ($)"] = pd.to_numeric(pipeline_by_rep["Total Pipeline ($)"], errors="coerce")
st.dataframe(pipeline_by_rep)

# Optional: Add a bar chart for visual impact
import altair as alt

# Optional: Add a labeled bar chart for visual impact
bar = alt.Chart(pipeline_by_rep).mark_bar().encode(
    x=alt.X("Rep:N", title="Sales Rep"),
    y=alt.Y("Total Pipeline ($):Q", title="Pipeline ($)")
).properties(
    title="Pipeline by Rep"
)

st.altair_chart(bar, use_container_width=True)


# -------------------------------
# Pipeline Stage Distribution
# -------------------------------
st.header("📊 Opportunity Stage Breakdown")
st.bar_chart(opps["stage"].value_counts())

# -------------------------------
# Forecast Summary
# -------------------------------
st.header("📈 Forecasting")
st.write("Weighted pipeline by probability")

opps["weighted_amount"] = opps["amount"] * (opps["probability"] / 100)
forecast = opps.groupby("stage")["weighted_amount"].sum().reset_index()
forecast.columns = ["Stage", "Weighted Pipeline ($)"]
st.dataframe(forecast)

st.header("🧠 Key Insights")

st.markdown(f"**🏆 Top Performer:** {insights['top_rep_total']} has the highest total and forecast-weighted pipeline.")
st.markdown(f"**🌱 Most Common Lead Source:** {insights['top_source']}")
st.markdown(f"**🎯 Best-Converting Source:** {insights['top_conversion_source']} — highest conversion to opportunity.")
st.markdown(f"**🐢 Longest-Stage Bottleneck:** {insights['longest_stage']} stage has the longest average time-in-stage.")

if pd.isna(insights['recent_avg_pipeline']):
    st.markdown("**📉 No new opportunities created in the past 30 days.**")
else:
    st.markdown(f"**📈 Recent Avg Pipeline Value:** ${insights['recent_avg_pipeline']:.2f} (last 30 days)")
