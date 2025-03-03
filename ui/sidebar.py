import streamlit as st

def show_sidebar():
    """Creates a styled sidebar navigation menu with a fixed, always open sidebar."""
    
    st.markdown("""
        <style>
            /* Sidebar Main Styling */
            [data-testid="stSidebar"] {
                background-color: #f8f9fa !important;
                padding: 15px;
                border-right: 2px solid #ddd;
                position: fixed;
                top: 61px;
                height: calc(100vh - 61px);
                width: 300px !important;
                box-shadow: 2px 0px 10px rgba(0,0,0,0.2);
            }

            /* Sidebar Title */
            .sidebar-title {
                font-size: 18px;
                font-weight: bold;
                color: #000000 !important;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
            }

            /* Sidebar Navigation Buttons */
            .sidebar-item {
                display: flex;
                align-items: center;
                font-size: 16px;
                padding: 12px;
                border-radius: 8px;
                text-decoration: none;
                color: #ffffff !important;
                font-weight: 500;
                background: #000000 !important;
                border: none;
                text-align: left;
                width: 100%;
                cursor: pointer;
                transition: background 0.3s ease-in-out, color 0.3s ease-in-out;
            }

            /* Sidebar Button Hover Effect */
            .sidebar-item:hover {
                background: #333333 !important;
            }

            /* Active Item */
            .sidebar-active {
                background: #ff6b6b !important;
                color: white !important;
                font-weight: bold !important;
                box-shadow: inset 0px 0px 8px rgba(0, 0, 0, 0.1);
            }

            /* ✅ Remove Sidebar Collapse Button */
            [data-testid="collapsedControl"] {
                display: none !important;
            }

            /* ✅ Remove any extra close button */
            [data-testid="stSidebarNav"] button {
                display: none !important;
            }

            /* ✅ Modify Radio Button Styles (Make Unselected White) */
            div[data-baseweb="radio"] > div {
                color: black !important;  /* Text color */
            }

            div[data-baseweb="radio"] svg {
                fill: white !important;  /* Unselected radio pill is now white */
            }

            div[data-baseweb="radio"]:has(input:checked) svg {
                fill: red !important; /* Selected radio pill remains red */
            }

        </style>
    """, unsafe_allow_html=True)

    # Sidebar Header
    st.sidebar.markdown('<div class="sidebar-title">📌 Main Menu</div>', unsafe_allow_html=True)

    # Sidebar Navigation
    options = {
        "🏠 Home": "Home",
        "📊 Advanced": "Advanced",
        "💬 ChatBot": "ChatBot",
        "✉️ Contact": "Contact",
        "ℹ️ About": "About"
    }

    selected_page = st.sidebar.radio("", list(options.keys()), index=0)

    return options[selected_page]
