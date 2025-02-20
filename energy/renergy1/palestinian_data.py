

import streamlit as st
import pandas as pd
import plotly.express as px



def apply_home_theme():
    st.markdown("""
        <style>
            .stApp {
                background-color: #1E1E2F !important; /* Deep blue energy-focused theme */
                color: #E0E0E0 !important;
            }
            [data-testid="stSidebar"] {
                background-color: #29293D !important;
            }
            [data-testid="stSidebar"] * {
                color: #E0E0E0 !important;
            }
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                color: #F4F4F9 !important;
            }
            .stPlotlyChart div {
                background-color: #1E1E2F !important;
            }
            .stSelectbox, .stTextInput, .stButton, .stCheckbox {
                background-color: #3A3A55 !important;
                border-radius: 5px !important;
                color: white !important;
            }
            html, body, [class*="st-"] {
                font-family: 'Arial', sans-serif;
            }
        </style>
    """, unsafe_allow_html=True)

apply_home_theme()

def app():
    st.markdown("<h1 style='text-align: center;'>Climate Changes and Renewable Energy in Palestine</h1>", unsafe_allow_html=True)

    file_path = "data_cleaned.csv"
    df = pd.read_csv(file_path)

    df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
    df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
    df = df.dropna(subset=["LAT", "LON"])

    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce").astype("Int64")
    df["MO"] = pd.to_numeric(df["MO"], errors="coerce").astype("Int64")

    city_mapping = {
        (31.5, 34.375): "Gaza",
        (31.5, 35.5): "Jericho",
        (31.5, 35.500): "Hebron",
        (32.0, 35.500): "Nablus",
        (32.5, 35.500): "Jenin",
        (32, 35.0): "Qalqilya",
        (32.5, 35.00): "Tulkarm",
    }

    df["City"] = df.apply(lambda row: city_mapping.get((row["LAT"], row["LON"]), "Unknown"), axis=1)

    st.sidebar.header("Climate Data in Palestinian Cities")
    _variable = st.sidebar.selectbox(
        "Choose a climate variable",
        ["Temperature", "Wind Speed", "UV Index", "Solar Radiation"]
    )

    variable_mapping = {
        "Temperature": "T2M",
        "Wind Speed": "WS2M",
        "UV Index": "ALLSKY_SFC_UV_INDEX",
        "Solar Radiation": "ALLSKY_SFC_SW_DWN"
    }

    selected_variable = variable_mapping[_variable]

    st.sidebar.header("Data Analysis by City")
    city_choice = st.sidebar.selectbox(
        "Choose a city",
        sorted([city for city in df["City"].unique() if city != "Unknown"])  
)


    df_filtered = df[df["City"] == city_choice]

    yearly_data = df_filtered[df_filtered["YEAR"].between(2020, 2024)]
    yearly_grouped = yearly_data.groupby("YEAR")[selected_variable].mean().reset_index()

    monthly_data = df_filtered[df_filtered["MO"].between(1, 12)]
    monthly_grouped = monthly_data.groupby("MO")[selected_variable].mean().reset_index()

    st.subheader(f"Climate Data in {city_choice}")

    fig_map = px.scatter_mapbox(
        df,
        lat="LAT",
        lon="LON",
        color=selected_variable,
        size_max=15,
        hover_name=selected_variable,
        hover_data=["City", "LAT", "LON", selected_variable],
        color_continuous_scale="plasma",
        mapbox_style="open-street-map",
        zoom=6,
    )

    fig_map.update_layout(
        mapbox=dict(style="open-street-map"),
        paper_bgcolor="#1E1E2F",
        plot_bgcolor="#1E1E2F",
        font=dict(color="#F4F4F9")
    )

    st.plotly_chart(fig_map, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_yearly = px.line(
            yearly_grouped,
            x="YEAR",
            y=selected_variable,
            labels={"YEAR": "Year", selected_variable: _variable},
            title=f"Yearly {_variable} Trends in {city_choice}"
        )
        fig_yearly.update_layout(
            paper_bgcolor="#1E1E2F",
            plot_bgcolor="#3A3A55",
            font=dict(color="white")
        )
        st.plotly_chart(fig_yearly, use_container_width=True)

    with col2:
        fig_monthly = px.line(
            monthly_grouped,
            x="MO",
            y=selected_variable,
            labels={"MO": "Month", selected_variable: _variable},
            title=f"Monthly {_variable} Trends in {city_choice}"
        )
        fig_monthly.update_layout(
            paper_bgcolor="#1E1E2F",
            plot_bgcolor="#3A3A55",
            font=dict(color="white")
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

    st.markdown(f"## Comparing {_variable} with Other Palestinian Cities")

    unique_locations = df.groupby("City").agg({selected_variable: 'mean'}).reset_index()

    fig3 = px.bar(
        unique_locations,
        x="City",
        y=selected_variable,
        labels={"City": "City", selected_variable: _variable},
        title=f"{_variable} in Each City"
    )
    fig3.update_layout(
        paper_bgcolor="#1E1E2F",
        plot_bgcolor="#3A3A55",
        font=dict(color="white")
    )
    st.plotly_chart(fig3, use_container_width=True)

    energy_summary = df.groupby("City").agg(
        Solar_Energy=("ALLSKY_SFC_SW_DWN", "sum"),
        Wind_Energy=("WS50M", "sum")
    ).reset_index()

    total_solar = energy_summary["Solar_Energy"].sum()
    total_wind = energy_summary["Wind_Energy"].sum()

    energy_distribution = pd.DataFrame({
        "Energy Source": ["Solar Energy", "Wind Energy"],
        "Total Usage": [total_solar, total_wind]
    })

    fig_pie = px.pie(
        energy_distribution,
        names="Energy Source",
        values="Total Usage",
        title="Wind vs. Solar Energy Distribution",
        color_discrete_sequence=["#27AE60", "#2980B9"]
    )

    fig_pie.update_layout(
        paper_bgcolor="#1E1E2F",
        plot_bgcolor="#3A3A55",
        font=dict(color="white")
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    if st.checkbox("Show Energy Data"):
        st.write(energy_summary[energy_summary["City"] == city_choice])
    def _suggestions(city):
        suggestions = ""

        if city in ["Jericho", "Hebron", "Gaza"]:
            suggestions += f"### {city} has high temperature levels\n"
            suggestions += "- High consumption (for air conditioning and cooling systems).\n"
            suggestions += "- High consumption → Higher pressure on electric grids (leading to higher costs and possible shortages).\n"
            suggestions += "- **Solution:** More heat → More sunlight → Use solar to generate electricity via solar panels.\n"

        if city in ["Nablus", "Jenin", "Tulkarm"]:
            suggestions += f"\n### {city} has strong and consistent wind\n"
            suggestions += "- This is due to its high altitude and coastal nature.\n"
            suggestions += "- Therefore, it is ideal for wind farms.\n"
            suggestions += "- Wind farms play a major role in wind production.\n"
            suggestions += "- **Solution:** Invest in wind farms to generate renewable energy and reduce grid dependency.\n"

        if city in ["Hebron", "Jericho", "Bethlehem"]:
            suggestions += f"\n### {city} experiences high UV index levels\n"
            suggestions += "- Prolonged UV exposure can weaken solar panels over time, reducing efficiency.\n"
            suggestions += "- **Solution:** Install UV-resistant solar panels to extend lifespan and maintain efficiency.\n"
            suggestions += "- Use reflective surfaces and shading techniques to reduce heat absorption.\n"

        if city in ["Jericho", "Gaza", "Qalqilya"]:
            suggestions += f"\n### {city} receives intense solar radiation\n"
            suggestions += "- This is beneficial for maintaining a reliable source of solar energy.\n"
            suggestions += "- **Suggested solutions:**\n"
            suggestions += "  - Build large-scale solar farms to maximize production.\n"
            suggestions += "  - Implement battery storage systems to store excess solar for nighttime use.\n"

        return suggestions

    st.markdown(f"## Tips on How to Conserve More Renewable Energy in {city_choice}")
    st.markdown(_suggestions(city_choice))

app()