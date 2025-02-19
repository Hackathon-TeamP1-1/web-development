import streamlit as st
import pandas as pd
import plotly.express as px

def show_solar_energy():
    df = pd.read_csv("data_cleaned.csv")

    solar_column = "ALLSKY_SFC_SW_DWN"  # Update based on your dataset
    max_year = df.loc[df[solar_column].idxmin(), "YEAR"]

    custom_colors = ["#F4A298", "#E57368", "#D9534F", "#A6192E", "#700019"]

    fig = px.pie(df, values=solar_column, names="YEAR",
                 color_discrete_sequence=custom_colors,
                 width=600, height=600, template="plotly_white")

    pull_values = [0.1 if year == max_year else 0 for year in df["YEAR"]]

    fig.update_traces(textposition='inside',
                      textinfo='percent+label',
                      pull=pull_values,
                      title="Solar Energy Consumption Distribution by Year",
                      insidetextfont=dict(size=16, color='white'))

    st.plotly_chart(fig, use_container_width=True)
