import streamlit as st

def show_header():
    st.markdown("""
        <style>
            /* Hide Default Streamlit Header */
            header {visibility: hidden;}

            /* Custom Header Styling */
            .custom-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 100%;
                height: 60px;
                padding: 10px 20px;
                background-color: #FFFFFF;
                color: #000000;
                font-size: 20px;
                font-weight: bold;
                position: fixed;
                top: 0;
                left: 0;
                z-index: 9999;
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
                background-color: #000000 !important;
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
        </style>
        <div class="custom-header">
            <div class="header-title">🌞 Renewable Energy Consumption Tracker</div>
            <div class="header-buttons">
                <button onclick="window.location.href='#login'">Login</button>
                <button onclick="window.location.href='#signup'">Signup</button>
            </div>
        </div>
    """, unsafe_allow_html=True)
