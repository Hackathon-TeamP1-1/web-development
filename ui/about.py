import streamlit as st

def show_about():
    st.subheader("ℹ️ About This App")
    
    # App Overview
    st.markdown("""
    **Renewable Energy Consumption Tracker** is a web application designed to visualize and predict renewable energy consumption trends. 
    It utilizes historical energy usage data and machine learning models to forecast future energy consumption.
    """)
    
    # Key Features
    st.markdown("""
    ### 🔥 Key Features:
    - 📊 **Data Visualization**: Displays historical and predicted renewable energy consumption trends.
    - 🔮 **Energy Prediction**: Uses AI/ML models to forecast energy consumption based on climate parameters.
    - 🌍 **Geospatial Insights**: Analyzes energy usage patterns across different locations.
    - 🔎 **Comparative Analysis**: Compares actual vs. predicted energy consumption to identify trends.
    - 📈 **Interactive Charts**: Provides graphical insights for better decision-making.
    """)
    
    # Technical Details
    st.markdown("""
    ### 🛠 Technical Details:
    - **Backend**: Python (Flask API) for handling machine learning predictions.
    - **Frontend**: Streamlit for interactive UI and data visualization.
    - **Machine Learning**: Uses regression models for energy forecasting.
    - **Data Sources**: Historical energy consumption data from various sources.
    """)
    
    # References & Data Sources
    st.markdown("""
    ### 📚 References & Data Sources:
    - 🌍 [World Bank Data](https://data.worldbank.org/) - Global energy consumption data.
    - ⚡ [NASA Power](https://power.larc.nasa.gov/) - Solar and wind energy datasets.
    - 🔢 [DataCamp](https://www.datacamp.com/) - AI & ML tutorials for energy forecasting.
    - 📊 [Kaggle Renewable Energy Datasets](https://www.kaggle.com/) - Public datasets for renewable energy.
    - 📖 [Streamlit Documentation](https://docs.streamlit.io/) - Guide to building interactive applications.
    """)

# Run the About page
if __name__ == "__main__":
    show_about()