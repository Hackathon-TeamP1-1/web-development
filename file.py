import streamlit as st
import pandas as pd 
import plotly.express as px 
import matplotlib.pyplot as plt


#from dash import Dash, dcc, html, Input, Output, callback

# read Data from excel 

 
df =pd.read_csv("data_cleaned.csv")
# st.write(df) 


# Streamlit UI
st.title("📊 Renewable Energy Consumption Tracker")
st.markdown("Graphical representation of renewable energy consumption")




# Streamlit UI

 
# WS2M wind Speed 
fig = px.pie(df, values="WS2M", names="YEAR"
  , color_discrete_sequence=px.colors.sequential.RdBu,width=600, height=600, template="plotly_dark"
    )
fig.update_traces(textposition='inside', 
                  textinfo='percent+label',
                  pull=[0, 0, 0.1, 0] * len(df) ,
                  title="Wind speed distribution by year",
                  insidetextfont=dict(size=16, color='white'),  
                
                 )

    
st.plotly_chart(fig, use_container_width=True)
# fig.show()  
