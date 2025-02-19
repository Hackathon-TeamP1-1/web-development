import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import requests


@st.cache_data
def load_data():
    csv_filename = "Country_Consumption_TWH.csv"

    if not os.path.exists(csv_filename):
        st.error(f" couldn't find `{csv_filename}` ")
        return None
    df = pd.read_csv(csv_filename)
    df.columns = df.columns.str.strip()
    df_long = df.melt(id_vars=["Year"], var_name="Country", value_name="Renewable__Consumption")

    return df_long

@st.cache_data
def load_geojson():
    geojson_filename = "world_countries.geojson"

    if not os.path.exists(geojson_filename):
        geojson_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
        response = requests.get(geojson_url)
        if response.status_code == 200:
            with open(geojson_filename, "w", encoding="utf-8") as file:
                file.write(response.text)
    with open(geojson_filename, "r", encoding="utf-8") as file:
        geojson_data = json.load(file)
    return geojson_data

def app():
    st.write("Renewable  consumption worldwide")
    df = load_data()
    geojson_data = load_geojson()

    st.markdown(
    """
    <style>
        /* whole background color */
        .stApp {
            background-color: #D4E6F1 !important;
        }
        /* Text Color */
        .stApp * {
            color: white !important;
        }

        /*  Sidebar Background Color */
        [data-testid="stSidebar"] {
            background-color: #154360 !important;
        }

        /* Sidebar Text Color */
        [data-testid="stSidebar"] * {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

    st.subheader("choose a country to view more details")
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson_data,
        locations="Country",
        featureidkey="properties.name",
        color="Renewable__Consumption",
        hover_name="Country",  
        color_continuous_scale="greens",
        mapbox_style="carto-positron",
        zoom=1.5,
        center={"lat": 20, "lon": 0},
    )
    fig.update_layout(
        mapbox=dict(
            style="open-street-map"),  
        paper_bgcolor="#D4E6F1",  
        plot_bgcolor="#154360",   
        font=dict(
            color="#154360"
        ),
        coloraxis_colorbar=dict(
            tickfont=dict(color="#154360"),
            title_font=dict(color="#154360")
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    selected_country = st.selectbox("choose a country", df["Country"].unique())
    df_country = df[df["Country"] == selected_country]
    st.subheader(f" more information about {selected_country}")

    fig_bar = px.bar(df_country, x="Year", y="Renewable__Consumption",
                     title="year vs. renewable  growth")

    fig_bar.update_layout(
        paper_bgcolor="#D4E6F1",  # chart bg out
        plot_bgcolor="#154360",  # chart bg in
        font=dict(color="white")  #chart inside color
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Renewable  Trends worldwide")
    fig_trend = px.line(df, x="Year", y="Renewable__Consumption", color="Country",
                        title="Renewable  Consumption over past years")

    # line chart(color)
    fig_trend.update_layout(
        paper_bgcolor="#D4E6F1",
        plot_bgcolor="#1C2833",  
        font=dict(color="white"),
        xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
        yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"))
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.subheader("most renewable  consuming countries")
    top_countries = df.groupby("Country").sum().reset_index().nlargest(10, "Renewable__Consumption")
    fig_top = px.bar(top_countries, x="Country", y="Renewable__Consumption",
                     title="Top 10 countries (according to their renewable  consumption)")

    # countries chart(back ground colors)
    fig_top.update_layout(
        paper_bgcolor="#D4E6F1",
        plot_bgcolor="#2E4053",  
        font=dict(color="white"),
        xaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white")),
        yaxis=dict(title_font=dict(color="white"), tickfont=dict(color="white"))
    )
    st.plotly_chart(fig_top, use_container_width=True)

if __name__ == "__main__":
    app()