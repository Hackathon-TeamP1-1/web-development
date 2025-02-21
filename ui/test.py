import streamlit as st
import requests

# Define the API endpoint
FLASK_API_URL = "http://127.0.0.1:5000"

# Function to check API connection
def check_api_status():
    try:
        response = requests.get(f"{FLASK_API_URL}/")
        if response.status_code == 200:
            st.success("✅ Flask API is running!")
            st.write("Response:", response.text)  # Show API response
        else:
            st.error("❌ Flask API is NOT reachable.")
    except requests.exceptions.RequestException as e:
        st.error(f"API connection failed: {e}")

# Streamlit UI
st.title("Flask API Connection Test")
if st.button("Check API Status"):
    check_api_status()
