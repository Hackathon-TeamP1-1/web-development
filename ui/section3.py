import streamlit as st
import requests

# Define the API endpoint
url = "https://b609-35-230-93-211.ngrok-free.app/predict"

# Example input data (modify as needed)
data = {
    "features": [[31.5, 34.5, 0.5, 2.0, 25.0, 60.0, 0.1, 0.6]]
}

def fetch_prediction(api_url, payload):
    try:
        # Send POST request
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return None

def show_section3():
    st.header("📊 Section 3")
    st.write("This section displays the prediction from the API.")

    # Fetch prediction from API
    result = fetch_prediction(url, data)

    if result:
        # Display the response in Streamlit
        st.subheader("Prediction Result:")
        st.write(result)
    else:
        st.error("Failed to retrieve prediction.")

# Run the Streamlit app
if __name__ == "__main__":
    show_section3()
