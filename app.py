import streamlit as st
import pandas as pd

st.set_page_config(page_title="RevOps Dashboard", layout="wide")

st.title("AI-Powered RevOps Dashboard")
st.write("This dashboard uses AI-generated mock data to simulate core RevOps metrics.")

# Load data
leads = pd.read_csv("data/leads.csv")
opps = pd.read_csv("data/opportunities.csv")

# Funnel tab
st.header("🔁 Funnel Overview")
st.subheader("Lead Stage Distribution")
st.bar_chart(leads["stage"].value_counts())

# Rep performance (basic placeholder)
st.header("👤 Rep Performance")
st.dataframe(opps.groupby("rep")["amount"].sum().reset_index().rename(columns={"amount": "Total Pipeline ($)"}))
