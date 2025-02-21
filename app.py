import streamlit as st
from ui.header import show_header
from ui.footer import show_footer
from ui.sidebar import show_sidebar
from ui.tchart import show_tchart
from ui.solar_energy import show_solar_energy
from ui.types import show_types
from ui.palestinian_data import show_palestinian_data
from ui.predict import show_predict
from ui.about import show_about
from ui.contact import show_contact


# ✅ Apply Global Styling
st.markdown("""
    <style>
        body, .stApp {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Display Header
show_header()

# ✅ Sidebar Navigation
page = show_sidebar()

# ✅ Home Page
if page == "Home":
    show_tchart()
    st.markdown("<br><br>", unsafe_allow_html=True)
    show_solar_energy()
    st.markdown("<br><br>", unsafe_allow_html=True)
    show_types()
    st.markdown("<br><br>", unsafe_allow_html=True)
    show_palestinian_data()

# ✅ Prediction Page
elif page == "Advanced":
    show_predict()

# ✅ Contact Page
elif page == "Contact":
    show_contact()

# ✅ About Page
elif page == "About":
    show_about()

# ✅ Footer
show_footer()
