import streamlit as st
import requests

# ✅ Ensure session state variables are initialized before access
if "show_signup" not in st.session_state:
    st.session_state["show_signup"] = False

def toggle_form():
    """Toggle between Login and Signup without refreshing the page"""
    st.session_state["show_signup"] = not st.session_state["show_signup"]

def show_auth_form():
    st.markdown(
        """
        <style>
            /* Centered Login/Signup Card */
            .auth-card {
                background-color: white;
                padding: 2rem;
                border-radius: 12px;
                max-width: 420px;
                margin: auto;
                text-align: left;
                font-family: 'Arial', sans-serif;
            }

            /* Header */
            .auth-header {
                font-size: 26px;
                font-weight: bold;
                margin-bottom: 20px;
                color: #333;
                display: flex;
                align-items: center;
                gap: 10px;
            }

            /* Input Fields */
            .auth-input {
                width: 100%;
                padding: 12px;
                margin-bottom: 15px;
                border-radius: 8px;
                border: 1px solid #ccc;
                font-size: 16px;
                background-color: #f8f9fa;
            }

            /* Full-Width Button */
            .auth-button {
                width: 100%;
                background-color: #28a745;
                color: white;
                border: none;
                padding: 14px;
                font-size: 18px;
                border-radius: 8px;
                cursor: pointer;
                transition: background-color 0.3s ease-in-out;
                text-align: center;
                font-weight: bold;
            }
            .auth-button:hover {
                background-color: #218838;
            }

            /* Centered Toggle Button */
            .toggle-container {
                text-align: center;
                margin-top: 15px;
            }
            .toggle-button {
                background: none;
                border: none;
                color: #007bff;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
                text-decoration: none;
                padding: 5px;
                display: inline-block;
            }
            .toggle-button:hover {
                text-decoration: underline;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create Auth Card
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)

    if st.session_state["show_signup"]:
        st.markdown("<div class='auth-header'>📝 Sign Up</div>", unsafe_allow_html=True)
        username = st.text_input("Username", key="signup_username")
        email = st.text_input("Email Address", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        # Full-Width Sign Up Button
        if st.button("Sign Up", key="signup_button", use_container_width=True):
            API_URL = "http://localhost:3030/api/auth/signup"
            try:
                response = requests.post(
                    API_URL,
                    json={"username": username, "email": email, "passwordHash": password},
                    timeout=5
                )
                if response.status_code == 201:
                    st.success("✅ Account Created! Please log in.")
                    st.session_state["show_signup"] = False  # Switch back to login
                    st.rerun()  # ✅ This refreshes the UI immediately
                else:
                    st.error(f"❌ Sign Up failed: {response.status_code} {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"🚨 API Error: {e}")
    else:
        st.markdown("<div class='auth-header'>🔑 Login</div>", unsafe_allow_html=True)
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        # Full-Width Login Button
        if st.button("Login", key="login_button", use_container_width=True):
            API_URL = "http://localhost:3030/api/auth/login"
            try:
                response = requests.post(
                    API_URL,  
                    json={"username": username, "passwordHash": password},
                    timeout=5
                )
                if response.status_code == 200:
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = response.json()
                    st.session_state["page"] = "Home"
                    st.success("✅ Login Successful! Redirecting...")
                    st.rerun()
                else:
                    st.error(f"❌ Login failed: {response.status_code} {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"🚨 API Error: {e}")

    # ✅ Toggle Button (Styled)
    toggle_text = "Already have an account? Login" if st.session_state["show_signup"] else "Don't have an account? Sign Up"
    st.markdown(
        f"""
        <div class="toggle-container">
            <button class="toggle-button" onclick="toggle_form()">{toggle_text}</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ✅ Hidden Streamlit Button (Ensures Toggle Works)
    if st.button("", key="hidden_toggle_button", use_container_width=False):
        toggle_form()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
