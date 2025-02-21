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
from ui.chatting import show_chat

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

# ✅ Page Routing
if page == "Home":
    show_tchart()
    st.markdown("<br><br>", unsafe_allow_html=True)
    show_solar_energy()
    st.markdown("<br><br>", unsafe_allow_html=True)
    show_types()
    st.markdown("<br><br>", unsafe_allow_html=True)
    show_palestinian_data()

elif page == "Advanced":
    show_predict()

elif page == "ChatBot":
    show_chat()  

elif page == "Contact":
    show_contact()

elif page == "About":
    show_about()

# ✅ Footer
show_footer()
