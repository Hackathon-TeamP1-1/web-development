import streamlit as st
import pandas as pd
import plotly.express as px

def show_solar_energy():
    # Load dataset
    df = pd.read_csv("data_cleaned.csv")

    # Column to use for the pie chart
    solar_column = "ALLSKY_SFC_SW_DWN"  # Keep the original column name

    # Ensure the column exists in the dataset
    if solar_column not in df.columns:
        st.error(f"⚠️ Column '{solar_column}' not found in dataset.")
        return

    # Find the year with the **minimum solar radiation**
    max_year = df.loc[df[solar_column].idxmin(), "YEAR"]

    # Custom color palette
    custom_colors = ["#F4A298", "#E57368", "#D9534F", "#A6192E", "#700019"]

    # Rename the column for better display in the chart
    df = df.rename(columns={solar_column: "Solar Radiation (W/m²)"})

    # Create Pie Chart
    fig = px.pie(df, values="Solar Radiation (W/m²)", names="YEAR",
                 color_discrete_sequence=custom_colors,
                 width=600, height=600, template="plotly_white")

    # Highlight the lowest year
    pull_values = [0.1 if year == max_year else 0 for year in df["YEAR"]]

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        pull=pull_values,
        title="Solar Energy Production Distribution by Year",
        insidetextfont=dict(size=16, color='white')
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
