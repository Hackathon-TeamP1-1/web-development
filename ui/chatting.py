# chatting.py
import streamlit as st

def show_chat():
    # Initialize session state for chat visibility and messages
    if 'chat_visible' not in st.session_state:
        st.session_state['chat_visible'] = False
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # Function to toggle chat visibility
    def toggle_chat():
        st.session_state['chat_visible'] = not st.session_state['chat_visible']

    # Display the chat window based on session state
    if st.session_state['chat_visible']:
        with st.container():
            st.markdown("""
                <style>
                    .chat-container {
                        position: fixed;
                        top: 60px;
                        right: 0;
                        width: 300px;
                        height: 400px;
                        background-color: #FFFFFF;
                        border: 1px solid #DDDDDD;
                        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2);
                        z-index: 9998;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                    }
                    .chat-messages {
                        padding: 10px;
                        flex-grow: 1;
                        overflow-y: auto;
                    }
                    .chat-input {
                        padding: 10px;
                        border-top: 1px solid #DDDDDD;
                    }
                </style>
                <div class="chat-container" id="chat-container">
                    <div class="chat-messages" id="chatMessages">
                        <!-- Chat messages will appear here -->
                        {}
                    </div>
                    <div class="chat-input">
                        <input type="text" id="chatInput" placeholder="Type a message..." style="width: 100%;">
                    </div>
                </div>
            """.format(
                ''.join(
                    f'<div><strong>{msg["role"]}:</strong> {msg["content"]}</div>'
                    for msg in st.session_state['messages']
                )
            ), unsafe_allow_html=True)

            # JavaScript to handle sending messages
            st.markdown("""
                <script>
                    const chatInput = document.getElementById('chatInput');
                    chatInput.addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            const message = chatInput.value;
                            if (message.trim() !== '') {
                                // Send the message to Streamlit
                                fetch('/send_message', {
                                    method: 'POST',
                                    body: JSON.stringify({message: message}),
                                    headers: {
                                        'Content-Type': 'application/json'
                                    }
                                }).then(() => {
                                    chatInput.value = '';
                                    // Trigger Streamlit rerun to update chat messages
                                    window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:rerun'}, '*');
                                });
                            }
                        }
                    });
                </script>
            """, unsafe_allow_html=True)
