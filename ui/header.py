import streamlit as st

def show_header():
    """Display a fixed full-width header with a title and buttons."""
    st.markdown("""
        <style>
            /* Hide Default Streamlit Header */
            header { visibility: hidden; }

            /* Custom Header Styling */
            .custom-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 100%;
                height: 60px;
                padding: 10px 20px;
                background-color: #FFFFFF; /* White Background */
                color: #000000; /* Black Text */
                font-size: 20px;
                font-weight: bold;
                position: fixed;
                top: 0;
                left: 0;
                z-index: 9999;  /* Ensure it's above everything */
                box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2);
            }

            .header-title {
                flex-grow: 1;
                text-align: left;
                font-size: 24px;
            }

            .header-buttons {
                display: flex;
                gap: 15px;
            }

            .header-buttons button {
                background-color: #000000 !important; /* Black Button */
                border: none;
                color: white;
                padding: 8px 15px;
                font-size: 14px;
                border-radius: 5px;
                cursor: pointer;
            }

            .header-buttons button:hover {
                background-color: #444444 !important;
            }

            /* Sidebar Button */
            .sidebar-toggle {
                position: absolute !important;
                bottom: 20px !important;
                left: 20px !important;
                z-index: 100; /* Keep it below the header */
                background: white;
                border-radius: 20px;
                padding: 10px;
                width: 45px;
                height: 45px;
                box-shadow: 0px 0px 6px rgba(0, 0, 255, 0.5);
                border: 2px solid blue;
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: pointer;
            }

        </style>
        <div class="custom-header">
            <div class="header-title">🌞 Renewable Energy Tracker</div>
            <div class="header-buttons">
                <button onclick="window.location.href='#login'">Login</button>
                <button onclick="window.location.href='#signup'">Signup</button>
                <button onclick="window.location.href='#chatbot'">💬</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Add spacing to ensure the content is not covered by the header
    st.markdown("<br><br>", unsafe_allow_html=True)
