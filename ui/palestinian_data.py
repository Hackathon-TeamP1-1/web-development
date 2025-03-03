import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from scipy.spatial import KDTree

# **FLASK API Endpoint for Predictions**
API_URL = "http://127.0.0.1:5000/predict"

# **Load Dataset**
file_path = "data_cleaned.csv"
df = pd.read_csv(file_path)

# **Define City Coordinates**
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
    "Rafah": (31.2870, 34.2590),
    "Khan Younis": (31.3400, 34.3060),
    "Salfit": (32.0820, 35.1822),
    "Jerusalem": (31.7683, 35.2137),
    "Tubas": (32.3200, 35.3686)
}

# **Convert dataset LAT, LON into KDTree for fast lookup**
coords = df[['LAT', 'LON']].values
tree = KDTree(coords)

# **Find the closest data point for a city**
def find_nearest_data(city_name):
    if city_name in city_mapping:
        lat, lon = city_mapping[city_name]
        _, idx = tree.query([lat, lon])  # Find the nearest data point
        return df.iloc[idx]
    return None

# **Fetch Prediction from Flask API**
def fetch_prediction(payload):
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()  # Return prediction
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API request failed: {e}")
        return None

# **Main Function to Display Climate Data & Predictions**
def show_palestinian_data():
    """Displays climate data and fetches predictions from Flask API."""

    # 1️⃣ **Dropdown Filters**
    st.subheader("📊 Climate Data Selection")
    climate_variable = st.selectbox("Choose a Climate Variable", ["Temperature", "Wind Speed", "UV Index", "Solar Radiation"])
    city_choice = st.selectbox("Choose a City", ["All Palestine"] + list(city_mapping.keys()))

    # **Variable Mapping**
    variable_mapping = {
        "Temperature": "T2M",
        "Wind Speed": "WS2M",
        "UV Index": "ALLSKY_SFC_UV_INDEX",
        "Solar Radiation": "ALLSKY_SFC_SW_DWN"
    }
    selected_variable = variable_mapping[climate_variable]

    # 2️⃣ **Map View with Highlighted City**
    city_df = pd.DataFrame(city_mapping.items(), columns=["City", "Coords"])
    city_df["LAT"] = city_df["Coords"].apply(lambda x: x[0])
    city_df["LON"] = city_df["Coords"].apply(lambda x: x[1])
    city_df.drop(columns=["Coords"], inplace=True)

    city_df["Color"] = "red"  # Default all cities to red
    if city_choice != "All Palestine":
        city_df.loc[city_df["City"] == city_choice, "Color"] = "green"  # Highlight selected city

    fig_map = px.scatter_mapbox(
        city_df, lat="LAT", lon="LON", text="City", color="Color",
        color_discrete_map={"red": "red", "green": "green"},
        mapbox_style="carto-positron", zoom=7, height=500, width=900
    )
    fig_map.update_traces(marker=dict(size=10), selector=dict(mode="markers+text"))
    st.plotly_chart(fig_map, use_container_width=True)

    # 3️⃣ **Show Current (Old) Data Before Prediction**
    if city_choice == "All Palestine":
        old_value = df[selected_variable].mean()  # Compute average across dataset
        st.markdown("### 📌 Current (Old) Data:")
        st.success(f"🌍 Average Energy from {climate_variable} for All Palestine: **{old_value:.2f}**")
    else:
        city_data = find_nearest_data(city_choice)
        if city_data is not None:
            st.markdown("### 📌 Current (Old) Data:")
            st.success(f"**Energy from {climate_variable} for {city_choice}** (Lat: {city_data['LAT']}, Lon: {city_data['LON']}): **{city_data[selected_variable]:.2f}**")
        else:
            st.error(f"❌ No data found for {city_choice}. Try selecting another city.")

    # 4️⃣ **Auto Fetch Predictions**
    predictions = []
    if city_choice == "All Palestine":
        for city in city_mapping.keys():
            city_data = find_nearest_data(city)
            if city_data is not None:
                payload = {
                    "LAT": city_data["LAT"],
                    "LON": city_data["LON"],
                    "ALLSKY_SFC_SW_DWN": city_data["ALLSKY_SFC_SW_DWN"],
                    "WS2M": city_data["WS2M"],
                    "T2M": city_data["T2M"],
                    "RH2M": city_data["RH2M"],
                    "PRECTOTCORR": city_data["PRECTOTCORR"],
                    "ALLSKY_KT": city_data["ALLSKY_KT"]
                }
                result = fetch_prediction(payload)
                if result:
                    predictions.append(result["predicted_energy"])
        
        if predictions:
            avg_prediction = sum(predictions) / len(predictions)
            st.markdown("### 🔮 Prediction Result:")
            st.success(f"🌍 Predicted Energy from {climate_variable} for All Palestine: {avg_prediction:.2f} KW/m²")
        else:
            st.error("❌ No valid data found for Palestine-wide prediction.")
    else:
        if city_data is not None:
            payload = {
                "LAT": city_data["LAT"],
                "LON": city_data["LON"],
                "ALLSKY_SFC_SW_DWN": city_data["ALLSKY_SFC_SW_DWN"],
                "WS2M": city_data["WS2M"],
                "T2M": city_data["T2M"],
                "RH2M": city_data["RH2M"],
                "PRECTOTCORR": city_data["PRECTOTCORR"],
                "ALLSKY_KT": city_data["ALLSKY_KT"]
            }
            
            result = fetch_prediction(payload)
            if result:
                st.markdown("### 🔮 Prediction Result:")
                st.success(f"Predicted Energy from {climate_variable} for {city_choice}: {result['predicted_energy']:.2f} KW/m²")
            else:
                st.error("❌ Failed to retrieve prediction.")

    # 5️⃣ **Climate Trends**
    yearly_grouped = df.groupby("YEAR")[selected_variable].mean().reset_index()
    monthly_grouped = df.groupby("MO")[selected_variable].mean().reset_index()

    col1, col2 = st.columns(2)
    with col1:
        fig_yearly = px.line(yearly_grouped, x="YEAR", y=selected_variable, title=f"Yearly {climate_variable} Trends", markers=True)
        st.plotly_chart(fig_yearly, use_container_width=True)

    with col2:
        fig_monthly = px.line(monthly_grouped, x="MO", y=selected_variable, title=f"Monthly {climate_variable} Trends", markers=True)
        st.plotly_chart(fig_monthly, use_container_width=True)
