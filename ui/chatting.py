import streamlit as st
import requests

BACKEND_URL = "http://localhost:3000/api/chatbot/message"

def show_chat():
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Basic chat styling
    st.markdown("""
        <style>
            .chat-container {
                background-color: #F5F5F5;
                border-radius: 10px;
                border: 1px solid #CCCCCC;
                box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2);
                padding: 16px;
                margin-top: 24px;
                margin-bottom: 24px;
            }
            .chat-header {
                font-weight: bold;
                font-size: 18px;
                color: #000000;
                margin-bottom: 8px;
                border-bottom: 1px solid #CCCCCC;
                padding-bottom: 8px;
            }
            .chat-messages {
                background-color: #FFFFFF; 
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #ECECEC;
                max-height: 300px;
                overflow-y: auto;
                margin-bottom: 16px;
            }
            /* A flex row for the two buttons, left-aligned, with a 10px gap */
            .button-row {
                display: flex;
                flex-direction: row;
                justify-content: flex-start;
                align-items: center;
                gap: 10px; /* Gap between buttons */
            }
        </style>
    """, unsafe_allow_html=True)

    # Main container
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        # Header
        st.markdown('<div class="chat-header">🤖 What can I help with?</div>', unsafe_allow_html=True)
        
        # Display the chat messages
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
        for msg in st.session_state['messages']:
            st.markdown(f"**{msg['role']}:** {msg['content']}")
        st.markdown('</div>', unsafe_allow_html=True)

        # User input field
        user_message = st.text_input("Type your message:", key="chat_input")

        # Wrap the two buttons in a .button-row div so they're side by side
        st.markdown('<div class="button-row">', unsafe_allow_html=True)
        
        # "Send" button
        if st.button("Send", key="send_btn"):
            if user_message.strip():
                st.session_state['messages'].append({"role": "User", "content": user_message})
                try:
                    response = requests.post(
                        BACKEND_URL,
                        json={"message": user_message},
                        timeout=120
                    )
                    if response.status_code == 200:
                        bot_response = response.json().get("response", "⚠️ No response from chatbot.")
                    else:
                        bot_response = f"⚠️ Error: {response.status_code} - {response.text}"
                except requests.exceptions.RequestException as e:
                    bot_response = f"⚠️ Failed to connect to chatbot: {e}"

                st.session_state['messages'].append({"role": "Bot", "content": bot_response})
                st.rerun()

        # "New Chat" button
        if st.button("New Chat", key="clear_btn"):
            st.session_state['messages'] = []
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)  # Close .button-row

        st.markdown('</div>', unsafe_allow_html=True)  # Close .chat-container
