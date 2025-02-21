import streamlit as st

def show_sidebar():
    """Creates a styled sidebar navigation menu with full-width buttons and improved styling."""
    
    st.markdown("""
        <style>
            /* Sidebar Main Styling */
            [data-testid="stSidebar"] {
                background-color: #f8f9fa !important; /* Light gray background */
                padding: 15px;
                border-right: 2px solid #ddd;
                position: fixed;
                top: 61px;  /* Moves sidebar down */
                height: calc(100vh - 61px);
                width: 300px !important;
                box-shadow: 2px 0px 10px rgba(0,0,0,0.2);
            }

            /* Sidebar Container */
            .sidebar-container {
                padding: 10px;
            }

            /* Sidebar Title */
            .sidebar-title {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
            }

            .sidebar-title i {
                font-size: 22px;
                margin-right: 8px;
            }

            /* Sidebar Button Styling */
            .sidebar-item {
                display: flex;
                align-items: center;
                font-size: 16px;
                padding: 12px;
                border-radius: 8px;
                text-decoration: none;
                color: #333;
                font-weight: 500;
                background: none;
                border: none;
                text-align: left;
                width: 100%;
                cursor: pointer;
                transition: background 0.3s ease-in-out, color 0.3s ease-in-out;
            }

            /* Hover Effect */
            .sidebar-item:hover {
                background: #e9ecef;
                cursor: pointer;
            }

            /* Active Item (Highlighted) */
            .sidebar-active {
                background: #ff6b6b !important;
                color: white !important;
                font-weight: bold !important;
                box-shadow: inset 0px 0px 8px rgba(0, 0, 0, 0.1);
            }

            /* Icons */
            .sidebar-icon {
                margin-right: 10px;
                font-size: 18px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar Header
    st.sidebar.markdown('<div class="sidebar-title">📌 Main Menu</div>', unsafe_allow_html=True)

    # Sidebar Navigation
    options = {
        "🏠 Home": "Home",
        "📊 Advanced": "Advanced",
        "✉️ Contact": "Contact",
        "ℹ️ About": "About"
    }

    selected_page = st.sidebar.radio("", list(options.keys()), index=0)

    return options[selected_page]
