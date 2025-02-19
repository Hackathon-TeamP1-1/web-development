
import streamlit as st
import pandas as pd
import plotly.express as px



def app():
    st.title="climate changes and renewable  in Palestine"
    file_path = "data_cleaned.csv"
    df = pd.read_csv(file_path)

    df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
    df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
    df = df.dropna(subset=["LAT", "LON"])

    city_mapping = {
        (31.0, 34.000): "Gaza",
        (31.0, 35.000): "Jericho",
        (31.0, 35.500): "Hebron",
        (32.0, 35.000): "Nablus",
        (32.5, 35.500): "Jenin",
        (31.5, 35.250): "Ramallah",
        (32.0, 35.250): "Tulkarm",
        (31.75, 35.250): "Bethlehem"
    }


    df["City"] = df.apply(lambda row: city_mapping.get((row["LAT"], row["LON"]), "Unknown"), axis=1)
    st.sidebar.header("climate data in palestinian cities")
    main_variable = st.sidebar.selectbox(
        "choose a climate variable",
        ["Temperature at 2M", "Wind Speed at 2M", "UV Index", "Solar Radiation"]
    )

    variable_mapping = {
        "Temperature at 2M": "T2M",
        "Wind Speed at 2M": "WS2M",
        "UV Index": "ALLSKY_SFC_UV_INDEX",
        "Solar Radiation": "ALLSKY_SFC_SW_DWN"
    }

    selected_variable = variable_mapping[main_variable]

    st.sidebar.header("Data Analysis by City")
    city_choice = st.sidebar.selectbox(
        "Choose a city ",
        sorted(df["City"].unique())
    )


    selected_data = df[df["City"] == city_choice]

    st.subheader("climate data across palesine")

    fig = px.scatter_mapbox(
        df,
        lat="LAT",
        lon="LON",
        color=selected_variable,
        size_max=15,
        hover_name=selected_variable,
        hover_data=["City", "LAT", "LON", selected_variable],
        color_continuous_scale="viridis",
        mapbox_style="carto-positron",
        zoom=6.5,
    )

    fig.update_layout(
        mapbox=dict(style="open-street-map"),
        height=700,
        width=1000,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#D4E6F1",  
        plot_bgcolor="#154360",
        font=dict(color="#154360"),
        coloraxis_colorbar=dict(
            tickfont=dict(color="#154360"),
            title_font=dict(color="#154360")
        )
    )

    st.plotly_chart(fig, use_container_width=True)

 
    st.markdown(f"## {main_variable} changes in {city_choice}")

    fig2 = px.line(
        selected_data,
        x=selected_data.index,  
        y=selected_variable,
        labels={"value": main_variable, "index": "Time"},
        title=f"{main_variable} Changes Over the years in {city_choice}"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown(f"## Comparing {main_variable} with othen palestinian cities")

    unique_locations = df.groupby("City").agg({selected_variable: 'mean'}).reset_index()

    fig3 = px.bar(
        unique_locations,
        x="City",
        y=selected_variable,
        labels={"City": "City", selected_variable: main_variable},
        title=f"{main_variable} in City"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(f"## Tips on how to conserve more renewable  in {city_choice}")

    def _suggestions(city):
        suggestions = ""

        if city in ["Jericho", "Hebron", "Gaza"]:
            suggestions += f"### {city} has high temperature levels\n"
            suggestions += "- High  consumption (for air conditioning and cooling systems).\n"
            suggestions += "- High  consumption → Higher pressure on electric grids (leading to higher costs and possible  shortages).\n"
            suggestions += "- **Solution:** More heat → More sunlight → Use solar  to generate electricity via solar panels.\n"

        if city in ["Nablus", "Jenin", "Tulkarm"]:
            suggestions += f"\n### {city} has strong and consistent wind\n"
            suggestions += "- This is due to its high altitude and coastal nature.\n"
            suggestions += "- Therefore, it is ideal for wind farms.\n"
            suggestions += "- Wind farms play a major role in wind  production.\n"
            suggestions += "- **Solution:** Invest in wind farms to generate renewable  and reduce grid dependency.\n"

        if city in ["Hebron", "Jericho", "Bethlehem"]:
            suggestions += f"\n### {city} experiences high UV index levels\n"
            suggestions += "- Prolonged UV exposure can weaken solar panels over time, reducing efficiency.\n"
            suggestions += "- **Solution:** Install UV-resistant solar panels to extend lifespan and maintain efficiency.\n"
            suggestions += "- Use reflective surfaces and shading techniques to reduce heat absorption.\n"

        if city in ["Jericho", "Gaza", "Ramallah"]:
            suggestions += f"\n### {city} receives intense solar radiation\n"
            suggestions += "- This is beneficial for maintaining a reliable source of solar .\n"
            suggestions += "- Therefore, it's recommended to store this solar  to prevent it from going to waste.\n"
            suggestions += "- **Suggested solutions:**\n"
            suggestions += "  - Build large-scale solar farms to maximize  production.\n"
            suggestions += "  - Implement battery storage systems to store excess solar  for nighttime use.\n"

        return suggestions
    city_data = unique_locations[unique_locations["City"] == city_choice].iloc[0]
    st.markdown(_suggestions(city_choice))
