import streamlit as st
import pandas as pd
import plotly.express as px

def show_tchart():
    # Page Title
    st.markdown(
        "<h2 style='text-align: center; font-size: 34px;'>📊 Renewable Energy Consumption Tracker</h2> <br>",
        unsafe_allow_html=True
    )

    # Load CSV file
    try:
        df = pd.read_csv("data_cleaned.csv")
    except FileNotFoundError:
        st.error("⚠️ Error: The file 'data_cleaned.csv' was not found.")
        return

    # Standardize column names (strip spaces)
    df.columns = df.columns.str.strip()

    # Check if necessary columns exist
    required_columns = {"MO", "ALLSKY_SFC_SW_DWN"}
    if not required_columns.issubset(df.columns):
        st.error(f"⚠️ Missing columns in the data: {required_columns - set(df.columns)}")
        return

    # Convert 'MO' column to month names
    df["Month"] = pd.to_datetime(df["MO"], format='%m').dt.strftime('%B')

    # Define correct month order
    month_order = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]

    # Ensure 'Month' column is categorical with the correct order
    df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)

    # Rename column for clarity
    df["Energy Production (KW/m^2)"] = df["ALLSKY_SFC_SW_DWN"]

    # Remove invalid values
    df = df[df["Energy Production (KW/m^2)"] > 0]

    # Group values by month (average Production per month)
    df_grouped = df.groupby("Month", as_index=False)["Energy Production (KW/m^2)"].mean()
    df_grouped = df_grouped.sort_values("Month")

    # Plot data using Plotly
    fig = px.bar(
        df_grouped, x="Month", y="Energy Production (KW/m^2)",
        title="Renewable Energy Production by Month",
        color="Energy Production (KW/m^2)",
        color_continuous_scale="Viridis",
        text="Energy Production (KW/m^2)"  # Show values on bars
    )

    # Improve layout
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Energy Production (KW/m^2)",
        template="plotly_white",
        font=dict(size=14),
        margin=dict(l=40, r=40, t=40, b=40),
    )

    # Customize hover labels
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
