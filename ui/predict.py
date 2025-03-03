import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

# ✅ Define API endpoint
API_URL = "http://127.0.0.1:5000/predict"

# ✅ Load historical renewable energy data
@st.cache_data
def load_historical_data():
    df = pd.read_csv("data_cleaned.csv")  # Ensure file contains renewable energy data
    return df

# ✅ Function to fetch prediction
def fetch_prediction(api_url, payload):
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()  # Parse response
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API request failed: {e}")
        return None

# ✅ Function to display prediction page
def show_predict():
    st.header("📊 Renewable Energy Prediction")
    st.write("Enter climate and weather data to predict **renewable energy consumption**.")

    # Load historical data
    df = load_historical_data()

    # 🌍 **User Inputs for Climate Data**
    lat = st.number_input("🌍 Latitude", value=31.5)
    lon = st.number_input("📍 Longitude", value=34.5)
    solar_radiation = st.number_input("☀️ Solar Radiation (ALLSKY_SFC_SW_DWN)", value=250.0)
    wind_speed = st.number_input("💨 Wind Speed (WS2M)", value=3.6)
    temperature = st.number_input("🌡️ Temperature (T2M)", value=25.0)
    humidity = st.number_input("💧 Humidity (RH2M)", value=60.0)
    precipitation = st.number_input("🌧️ Precipitation (PRECTOTCORR)", value=0.5)
    kt = st.number_input("☀️ ALLSKY_KT", value=0.7)

    # ✅ Button to Get Prediction
    if st.button("🔮 Get Energy Prediction"):
        # Store input data
        input_data = {
            "LAT": lat,
            "LON": lon,
            "ALLSKY_SFC_SW_DWN": solar_radiation,
            "WS2M": wind_speed,
            "T2M": temperature,
            "RH2M": humidity,
            "PRECTOTCORR": precipitation,
            "ALLSKY_KT": kt
        }

        # **Fetch Prediction**
        result = fetch_prediction(API_URL, input_data)

        if result:
            predicted_energy = result["predicted_energy"]

            # 🎯 **Display Prediction Result**
            st.subheader("🔮 Prediction Result:")
            st.success(f"Predicted Renewable Energy Production: {predicted_energy:.2f} KW/m²")

            # Add space below the prediction result
            st.markdown("<br><br>", unsafe_allow_html=True)

            # ✅ **Fetch Historical Energy Consumption**
            historical_energy = df["ALLSKY_SFC_SW_DWN"].mean()  # Ensure this is the correct column

            # 📊 **Create a Comparison Chart**
            st.subheader("📈 Renewable Energy Consumption Comparison")

            labels = ["Historical Consumption", "Predicted Consumption"]
            values = [historical_energy, predicted_energy]

            # **Plot Data**
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.bar(labels, values, color=["blue", "green"], alpha=0.7, edgecolor="black")

            ax.set_ylabel("Energy Consumption (KW/m²)", fontsize=12)
            ax.set_title("Comparison of Actual vs Predicted Renewable Energy", fontsize=13, fontweight="bold")
            ax.grid(axis="y", linestyle="--", alpha=0.7)

            # ✅ **Show Chart**
            st.pyplot(fig)

        else:
            st.error("❌ Failed to retrieve prediction.")

# ✅ Run the Streamlit app
if __name__ == "__main__":
    show_predict()
