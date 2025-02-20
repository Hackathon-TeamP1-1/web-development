import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.spatial import KDTree  # Import for nearest neighbor search

def show_palestinian_data(climate_variable, city_choice):
    """Display dynamically updating climate data with real temperature values."""

    # ✅ **Load Data**
    file_path = "data_cleaned.csv"
    df = pd.read_csv(file_path)

    # ✅ **Clean Data**
    df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
    df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
    df.dropna(subset=["LAT", "LON"], inplace=True)
    df["YEAR"] = pd.to_numeric(df["YEAR"], errors="coerce").astype("Int64")
    df["MO"] = pd.to_numeric(df["MO"], errors="coerce").astype("Int64")

    # ✅ **City Mapping (More Accurate)**
    city_mapping = {
        "Gaza": (31.5241, 34.4500),
        "Jericho": (31.8667, 35.4500),
        "Hebron": (31.5333, 35.0950),
        "Nablus": (32.2211, 35.2544),
        "Jenin": (32.4595, 35.2951),
        "Qalqilya": (32.1967, 35.0131),
        "Tulkarm": (32.3156, 35.0286),
        "Bethlehem": (31.7054, 35.2024),
        "Ramallah": (31.9066, 35.2033),
        "Jerusalem": (31.7683, 35.2137),
        "Rafah": (31.2870, 34.2590),
        "Khan Younis": (31.3400, 34.3060)
    }

    # ✅ **Convert city mapping to DataFrame**
    city_df = pd.DataFrame(city_mapping.items(), columns=["City", "Coords"])
    city_df["LAT"] = city_df["Coords"].apply(lambda x: x[0])
    city_df["LON"] = city_df["Coords"].apply(lambda x: x[1])
    city_df.drop(columns=["Coords"], inplace=True)

    # ✅ **Climate Variable Mapping**
    variable_mapping = {
        "Temperature": "T2M",
        "Wind Speed": "WS2M",
        "UV Index": "ALLSKY_SFC_UV_INDEX",
        "Solar Radiation": "ALLSKY_SFC_SW_DWN"
    }
    selected_variable = variable_mapping[climate_variable]

    # ✅ **Get Min and Max for Denormalization**
    t2m_min = -10  # Set based on real temperature data
    t2m_max = 50   # Set based on real temperature data

    # ✅ **Find the Nearest Temperature Data for Each City**
    climate_data_points = df[["LAT", "LON", selected_variable]].dropna()
    climate_tree = KDTree(climate_data_points[["LAT", "LON"]].values)

    def find_nearest_temperature(lat, lon):
        """Finds the closest temperature data point and converts to Celsius."""
        _, idx = climate_tree.query([lat, lon])  # Find closest point
        normalized_temp = climate_data_points.iloc[idx][selected_variable]
        return normalized_temp * (t2m_max - t2m_min) + t2m_min  # **Denormalize Temperature**

    city_df[selected_variable] = city_df.apply(lambda row: find_nearest_temperature(row["LAT"], row["LON"]), axis=1)

    # ✅ **Assign Cities to df (Fix Hover Issue)**
    def assign_nearest_city(lat, lon):
        return min(city_mapping.keys(), key=lambda city: (lat - city_mapping[city][0])**2 + (lon - city_mapping[city][1])**2)

    df["City"] = df.apply(lambda row: assign_nearest_city(row["LAT"], row["LON"]), axis=1)

    # ✅ **Filter Data Based on Selection**
    if city_choice == "All Palestine":
        # Filter by proximity if 'All Palestine' is selected
        df_filtered = df[df[["LAT", "LON"]].apply(
            lambda row: any(
                abs(row["LAT"] - lat) < 0.1 and abs(row["LON"] - lon) < 0.1
                for lat, lon in city_mapping.values()
            ), axis=1
        )]  # Only keep relevant points
    else:
        # Check if city exists in city_mapping or not
        if city_choice in city_mapping:
            df_filtered = df[df["City"] == city_choice]  # Use the assigned city column
        else:
            # If city not in the dataset, find the closest coordinates
            selected_city_coords = city_mapping[city_choice]
            _, idx = climate_tree.query(selected_city_coords)
            df_filtered = df.iloc[[idx]]  # Get data for closest match

    if df_filtered.empty:
        st.error(f"❌ No data found for {city_choice}. Try selecting another city.")
        return  # Stop execution if no data is found

    # ✅ **Denormalize T2M for Plots**
    df_filtered[selected_variable] = df_filtered[selected_variable] * (t2m_max - t2m_min) + t2m_min
    yearly_grouped = df_filtered.groupby("YEAR")[selected_variable].mean().reset_index()
    monthly_grouped = df_filtered.groupby("MO")[selected_variable].mean().reset_index()

    # ✅ **🌍 Improved Map Visualization**
    fig_map = px.scatter_mapbox(
        df_filtered, lat="LAT", lon="LON", color=selected_variable, size_max=14,
        hover_name="City", hover_data=["LAT", "LON", selected_variable],
        color_continuous_scale="turbo",  # 🌈 Vibrant Color Scale
        mapbox_style="carto-positron",  # 🌍 Better readability
        opacity=0.8, zoom=7 if city_choice != "All Palestine" else 6, height=500, width=900
    )

    # ✅ **Add City Markers to the Map with Temperature-Based Coloring**
    fig_map.add_trace(
        px.scatter_mapbox(city_df, lat="LAT", lon="LON", text="City",
                          color=city_df[selected_variable], color_continuous_scale="turbo",
                          hover_data=["LAT", "LON", selected_variable]).data[0]
    )

    fig_map.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="white",
        font=dict(size=14)
    )

    # ✅ **📍 Set Dynamic Title**
    if city_choice == "All Palestine":
        st.markdown("## Climate Data in Palestine")
    else:
        st.markdown(f"## Climate Data in {city_choice}")

    st.plotly_chart(fig_map, use_container_width=True)

    # ✅ **📈 Yearly and Monthly Trends**
    col1, col2 = st.columns(2)
    with col1:
        fig_yearly = px.line(yearly_grouped, x="YEAR", y=selected_variable, title=f"Yearly {climate_variable} Trends",
                             markers=True, line_shape="spline")
        st.plotly_chart(fig_yearly, use_container_width=True)

    with col2:
        fig_monthly = px.line(monthly_grouped, x="MO", y=selected_variable, title=f"Monthly {climate_variable} Trends",
                              markers=True, line_shape="spline")
        st.plotly_chart(fig_monthly, use_container_width=True)
