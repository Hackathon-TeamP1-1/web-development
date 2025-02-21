import streamlit as st
import pandas as pd
import plotly.express as px

def show_types():
    """Create Section 4 for displaying a stacked area chart by year."""
    
    # Load CSV file
    df = pd.read_csv("data_cleaned.csv")

    # Ensure that necessary columns exist
    required_columns = {"YEAR", "ALLSKY_SFC_SW_DWN", "T2M", "WS2M", "ALLSKY_SFC_UV_INDEX"}
    if not required_columns.issubset(df.columns):
        st.error(f"Missing columns in the data: {required_columns - set(df.columns)}")
    else:
        # Prepare data for stacked area chart
        # Map the selected parameter to its corresponding column
        energy_sources = ["ALLSKY_SFC_SW_DWN", "T2M", "WS2M", "ALLSKY_SFC_UV_INDEX"]
        df_grouped = df.groupby("YEAR")[energy_sources].mean().reset_index()

        # Convert the data from wide format to long format
        df_long = df_grouped.melt(id_vars="YEAR", value_vars=energy_sources, var_name="Energy Source", value_name="Energy Consumption (MWh)")

        # Plotting the data as a stacked area chart
        fig = px.area(
            df_long,
            x="YEAR",
            y="Energy Consumption (MWh)",
            color="Energy Source",
            title="Renewable Energy Consumption by Year",
            labels={"Energy Consumption (MWh)": "Energy Consumption (MWh)", "YEAR": "Year"},
            color_discrete_sequence=["brown", "blue", "green", "orange"]
        )

        # Improve chart layout
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Energy Consumption (MWh)",
            template="plotly_dark"
        )

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

