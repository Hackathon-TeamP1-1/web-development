import streamlit as st
import pandas as pd
import plotly.express as px

def show_tchart():

    st.markdown(
        "<h2 style='text-align: center; font-size: 34px;'>📊 Renewable Energy Consumption Tracker</h2> <br>",
        unsafe_allow_html=True
    )

    # Load CSV file
    df = pd.read_csv("data_cleaned.csv")

    # Check if the necessary columns are present
    required_columns = {"MO", "ALLSKY_SFC_SW_DWN"}
    if not required_columns.issubset(df.columns):
        st.error(f"Missing columns in the data: {required_columns - set(df.columns)}")
    else:
        # Convert month numbers to names
        df["Month"] = pd.to_datetime(df["MO"], format='%m').dt.strftime('%B')

        # Define correct month order
        month_order = ["January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]

        # Ensure 'Month' column is categorical with the correct order
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
