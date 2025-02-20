# Import necessary libraries
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import requests

# Function to get weather forecast
def get_forecast_weather(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    next_day_forecast = data['list'][7]
    return {
        "T2M": next_day_forecast['main']['temp'],
        "WS2M": next_day_forecast['wind']['speed'],
        "RH2M": next_day_forecast['main']['humidity'],
        "ALLSKY_SFC_SW_DWN": 0.5,
        "PRECTOTCORR": next_day_forecast['pop'],
        "ALLSKY_KT": 0.6
    }

# Load dataset (needed to fit MinMaxScaler)
df = pd.read_csv("Data_loaded.csv")

# Define the features to scale
features = ["LAT", "LON", "ALLSKY_SFC_SW_DWN", "WS2M", "T2M", "RH2M", "PRECTOTCORR", "ALLSKY_KT"]

# Initialize and fit MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(df[features])  # Fit the scaler using the dataset

# Load the trained model
model = load_model('Energy_Forcasting.h5')

def predict_energy(lat, lon):
    """Predict energy production for given latitude and longitude."""
    api_key = "436200292fc50b6345c6ff1649378eb3"
    forecast_weather = get_forecast_weather(lat, lon, api_key)

    future_input_df = pd.DataFrame([{
        "LAT": lat,
        "LON": lon,
        "ALLSKY_SFC_SW_DWN": forecast_weather['ALLSKY_SFC_SW_DWN'],
        "WS2M": forecast_weather['WS2M'],
        "T2M": forecast_weather['T2M'],
        "RH2M": forecast_weather['RH2M'],
        "PRECTOTCORR": forecast_weather['PRECTOTCORR'],
        "ALLSKY_KT": forecast_weather['ALLSKY_KT']
    }])

    # Scale input data
    future_input_scaled = scaler.transform(future_input_df)
    future_input_scaled = np.expand_dims(future_input_scaled, axis=0)

    # Make prediction
    prediction = model.predict(future_input_scaled)[0][0]

    # Ensure prediction is non-negative
    return max(prediction, 0)  # Clip negative values

# ✅ Prevent code from running when imported
if __name__ == "__main__":
    lat, lon = 31.5, 34.5
    pred = predict_energy(lat, lon)
    print(f"Predicted Energy Production: {pred:.2f} kWh")
