import streamlit as st
import pandas as pd
import plotly.express as px

def show_types():
    """Create Section 4 for displaying a stacked area chart by year with parameter explanations."""
    
    # Load CSV file
    df = pd.read_csv("data_cleaned.csv")

    # Define parameter descriptions
    parameters = {
        "ALLSKY_SFC_SW_DWN": "Solar Radiation (ALLSKY_SFC_SW_DWN)",
        "T2M": "Temperature (T2M)",
        "WS2M": "Wind Speed (WS2M)",
        "ALLSKY_SFC_UV_INDEX": "UV Index (ALLSKY_SFC_UV_INDEX)"
    }
    # Define parameter descriptions
    parameter_descriptions = {
        "ALLSKY_SFC_SW_DWN": "Solar Radiation (ALLSKY_SFC_SW_DWN) - Measures total solar energy received at the surface (W/m²).",
        "T2M": "Temperature (T2M) - Measures air temperature at 2 meters above ground (°C).",
        "WS2M": "Wind Speed (WS2M) - Measures wind speed at 2 meters above ground (m/s).",
        "ALLSKY_SFC_UV_INDEX": "UV Index (ALLSKY_SFC_UV_INDEX) - Measures the ultraviolet radiation level at the surface."
    }

    # Ensure that necessary columns exist
    required_columns = set(parameter_descriptions.keys()).union({"YEAR"})
    if not required_columns.issubset(df.columns):
        st.error(f"Missing columns in the data: {required_columns - set(df.columns)}")
    else:
        # Prepare data for stacked area chart
        energy_sources = list(parameter_descriptions.keys())
        df_grouped = df.groupby("YEAR")[energy_sources].mean().reset_index()

        # Convert the data from wide format to long format
        df_long = df_grouped.melt(id_vars="YEAR", value_vars=energy_sources, var_name="Energy Source", value_name="Energy Consumption (MWh)")

        # Map energy sources to their descriptions
        df_long["Energy Source"] = df_long["Energy Source"].map(parameters)

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
