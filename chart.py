import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the Streamlit page
st.set_page_config(page_title="Renewable Energy Consumption Tracker", layout="wide")

# App title
st.title("📊 Renewable Energy Consumption Tracker")
st.markdown("### Monthly Renewable Energy Consumption Visualization")

# Load CSV file
df = pd.read_csv("data_cleaned.csv")

# Convert month numbers to names
df["Month"] = df["MO"].map({
    1: "January", 2: "February", 3: "March", 4: "April", 
    5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 
    10: "October", 11: "November", 12: "December"
})

# Define correct month order
month_order = ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]

df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)

# Select energy consumption column
df["Energy Consumption (MWh)"] = df["ALLSKY_SFC_SW_DWN"]

# Remove invalid values (e.g., negative or undefined values)
df = df[df["Energy Consumption (MWh)"] > 0]

# Group values by month (average consumption per month)
df_grouped = df.groupby("Month", as_index=False)["Energy Consumption (MWh)"].mean()
df_grouped = df_grouped.sort_values("Month")  # Ensure correct order

# Plot data using Plotly
fig = px.bar(
    df_grouped, x="Month", y="Energy Consumption (MWh)",
    title="Renewable Energy Consumption by Month",
    color="Energy Consumption (MWh)",
    color_continuous_scale="Viridis"
)

# Improve layout
fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Energy Consumption (MWh)",
    template="plotly_dark"
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

