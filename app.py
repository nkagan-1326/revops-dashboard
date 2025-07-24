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
