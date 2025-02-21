# header.py
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
            /* Chat Icon Styling */
            .chat-icon {
                width: 40px;
                height: 40px;
                cursor: pointer;
                border-radius: 50%;
                background-color: #0000FF;
                display: flex;
                justify-content: center;
                align-items: center;
                box-shadow: 0px 0px 6px rgba(0, 0, 255, 0.5);
                color: white;
                font-size: 22px;
                line-height: 40px;
                text-align: center;
                border: none;
            }
        </style>
        <div class="custom-header">
            <div class="header-title">🌞 Renewable Energy Consumption Tracker</div>
            <div class="header-buttons">
                <button onclick="window.location.href='#login'">Login</button>
                <button onclick="window.location.href='#signup'">Signup</button>
                <button class="chat-icon" onclick="toggleChat()">💬</button>
            </div>
        </div>
        <script>
            function toggleChat() {
                const chatWindow = document.getElementById('chat-container');
                if (chatWindow.style.display === 'none' || chatWindow.style.display === '') {
                    chatWindow.style.display = 'flex';
                } else {
                    chatWindow.style.display = 'none';
                }
                // Trigger Streamlit rerun to update session state
                window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:rerun'}, '*');
            }
        </script>
    """, unsafe_allow_html=True)

