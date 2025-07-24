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
st.dataframe(pipeline_by_rep)

# Optional: Add a bar chart for visual impact
st.bar_chart(pipeline_by_rep.set_index("Rep"))

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
