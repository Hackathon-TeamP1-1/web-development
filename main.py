import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from flask_ngrok import run_with_ngrok  # Import flask_ngrok

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when the app is run

# Load trained model
model = load_model('Energy_Forcasting.h5')

# Load dataset inside Flask to fit the scaler
df = pd.read_csv("Data_loaded.csv")

# Define the features to scale
features = ["LAT", "LON", "ALLSKY_SFC_SW_DWN", "WS2M", "T2M", "RH2M", "PRECTOTCORR", "ALLSKY_KT"]

# Fit the scaler inside Flask
scaler = MinMaxScaler()
scaler.fit(df[features])  # Fit the scaler only once

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Receive input features from request
        data = request.json["features"]  # Expecting 2D list [[feature1, feature2, ...]]

        # Convert input to NumPy array
        data = np.array(data).reshape(1, -1)  # Reshape to fit the scaler

        # Apply scaling
        scaled_data = scaler.transform(data)

        # Reshape for LSTM input format (sequence length=5, features=8)
        lstm_input = scaled_data.reshape(1, 5, 8)

        # Make prediction
        prediction = model.predict(lstm_input)[0][0]

        return jsonify({"predicted_energy": prediction})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run()
