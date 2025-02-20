import streamlit as st

def show_footer():
    """Display footer at the bottom of the page."""
    st.markdown("""
        <style>
            .footer-container {
                width: 100%;
                height: 40px;
                padding: 10px;
                position: fixed;
                bottom: 0;
                left: 0;
                background-color: #FFFFFF; /* White Background */
                color: #000000; /* Black Text */
                text-align: center;
                font-size: 14px;
            }
        </style>
        <div class="footer-container">
            © 2024 Renewable Energy Tracker | All Rights Reserved
        </div>
    """, unsafe_allow_html=True)
