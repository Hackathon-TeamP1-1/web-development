import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

# ✅ Define API endpoint
API_URL = "http://127.0.0.1:5000/predict"

# ✅ Load historical renewable energy data
@st.cache_data
def load_historical_data():
    try:
        df = pd.read_csv("data_cleaned.csv")  # Ensure file contains renewable energy data
        if df.empty:
            st.error("🚨 The dataset is empty. Please check your CSV file.")
            return None
        return df
    except Exception as e:
        st.error(f"🚨 Error loading historical data: {e}")
        return None

# ✅ Function to fetch prediction
def fetch_prediction(api_url, payload):
    try:
        response = requests.post(api_url, json=payload, timeout=10)  # Timeout to prevent hanging requests
        response.raise_for_status()  # Raise exception for HTTP errors

        # ✅ Ensure response is valid JSON
        result = response.json()
        if "predicted_energy" not in result:
            st.error("❌ API response does not contain 'predicted_energy'.")
            return None

        return result
    except requests.exceptions.ConnectionError:
        st.error("❌ Failed to connect to API. Is the backend running?")
        return None
    except requests.exceptions.Timeout:
        st.error("❌ API request timed out. The server might be too slow or overloaded.")
        return None
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

        if result and "predicted_energy" in result:
            predicted_energy = result["predicted_energy"]

            # 🎯 **Display Prediction Result**
            st.subheader("🔮 Prediction Result:")
            st.success(f"Predicted Renewable Energy Production: {predicted_energy:.2f} KW/m²")

            # ✅ **Fetch Historical Energy Consumption**
            if df is not None and "ALLSKY_SFC_SW_DWN" in df.columns:
                historical_energy = df["ALLSKY_SFC_SW_DWN"].mean()
            else:
                st.error("🚨 Historical energy data is missing or incorrectly formatted!")
                historical_energy = None

            # 📊 **Create a Comparison Chart**
            if historical_energy is not None and predicted_energy is not None:
                st.subheader("📈 Renewable Energy Consumption Comparison")
                st.write(f"Debug: historical_energy = {historical_energy}, predicted_energy = {predicted_energy}")

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
                st.warning("⚠️ Skipping comparison chart due to missing historical data.")

        else:
            st.error("❌ Failed to retrieve prediction.")

