import streamlit as st
from ui.header import show_header
from ui.footer import show_footer
from ui.sidebar import show_sidebar
from ui.climate_data import show_palestinian_data
from ui.solar_energy import show_solar_energy
from ui.tchart import show_tchart

# ✅ Apply Global Styling (White Background & Black Text)
st.markdown("""
    <style>
        body, .stApp {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        /* Adjust sidebar to stay under the header */
        section[data-testid="stSidebar"] {
            position: fixed;
            top: 20px; /* Same height as header */
            left: 0;
            width: 250px;
            height: calc(100vh - 60px);
            background-color: #FFFFFF; /* Sidebar background */
            padding: 15px;
            overflow-y: auto;
            box-shadow: 2px 0px 10px rgba(0,0,0,0.2);
        }
        section[data-testid="stSidebar"] * {
            color: #000000 !important; /* Sidebar text color */
        }
        /* Ensure main content is positioned next to sidebar */
        .main-content {
            margin-left: 270px; /* Sidebar width + margin */
            padding: 0 20px 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Display Header
show_header()

# ✅ Sidebar for Filters (returns selected values)
climate_variable, city_choice = show_sidebar()

show_tchart()
st.markdown("<br><br>", unsafe_allow_html=True)
show_solar_energy()

# ✅ Display Climate Data Based on Sidebar Selection
show_palestinian_data(climate_variable, city_choice)

# ✅ Footer (Fixed at Bottom)
show_footer()

st.markdown('</div>', unsafe_allow_html=True)
