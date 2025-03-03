import streamlit as st
import requests
from ui.auth import show_auth_form 

# ✅ Set Streamlit page configuration
st.set_page_config(
    page_title="Sumud",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded" 
)

# ✅ Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
    st.session_state["page"] = "login"  # Default to login/signup

if "user" not in st.session_state:
    st.session_state["user"] = None
    st.session_state["token"] = None

# ✅ Backend API URL
API_URL = "http://localhost:3030/api/auth"

# ✅ Check Backend Connection
def test_backend_connection():
    try:
        response = requests.head(API_URL, timeout=5)
        return response.status_code < 500
    except requests.exceptions.RequestException:
        return False

backend_running = test_backend_connection()

if not backend_running:
    st.title("🚨 Backend API is Down")
    st.error("🚨 Please start your ASP.NET Core server.")
    st.stop()

# ✅ Show Login/Signup Page Initially
if not st.session_state["authenticated"]:
    st.title("⚡ Welcome to Sumud!")
    show_auth_form()  # 🔄 Show login/signup form inside a card
    st.stop()  # Prevent further execution until user logs in

# ✅ If authenticated, render the full application
from ui.header import show_header
from ui.sidebar import show_sidebar
from ui.tchart import show_tchart
from ui.solar_energy import show_solar_energy
from ui.types import show_types
from ui.palestinian_data import show_palestinian_data
from ui.predict import show_predict
from ui.about import show_about
from ui.contact import show_contact
from ui.chatting import show_chat
from ui.footer import show_footer

# ✅ Show app layout
show_header()
selected_page = show_sidebar()  

if selected_page == "Home":
    show_tchart()
    show_solar_energy()
    show_types()
    show_palestinian_data()
elif selected_page == "Advanced":
    show_predict()
elif selected_page == "ChatBot":
    show_chat()
elif selected_page == "Contact":
    show_contact()
elif selected_page == "About":
    show_about()

show_footer()
