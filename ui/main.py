import streamlit as st
from ui.sidebar import show_sidebar
from ui.tchart import show_tchart
from ui.solar_energy import show_solar_energy
from ui.types import show_types
from ui.palestinian_data import show_palestinian_data
from ui.predict import show_predict
from ui.about import show_about
from ui.contact import show_contact
from ui.chatting import show_chat

def show_main():
    # ✅ Show Sidebar Only After Login
    show_sidebar()

    # ✅ Page Routing
    page = st.session_state.get("page", "Home")

    if page == "Home":
        show_tchart()
        show_solar_energy()
        show_types()
        show_palestinian_data()
    elif page == "Advanced":
        show_predict()
    elif page == "ChatBot":
        show_chat()
    elif page == "Contact":
        show_contact()
    elif page == "About":
        show_about()
