import streamlit as st
import ollama
import PyPDF2
import os
import torch
import re

# ✅ Define Constants
PDF_FILE = "details.pdf"
VAULT_FILE = "vault.txt"

# ✅ Extract Text from PDF and Save to Vault
def load_pdf():
    if not os.path.exists(PDF_FILE):
        st.error("🚨 Error: `details.pdf` not found.")
        return "Error: `details.pdf` not found."

    with open(PDF_FILE, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = " ".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

    text = re.sub(r'\s+', ' ', text).strip()

    with open(VAULT_FILE, "w", encoding="utf-8") as vault:
        vault.write(text)

    return text

# ✅ Generate Embeddings for RAG
def generate_embeddings():
    if not os.path.exists(VAULT_FILE):
        st.warning("⚠️ No data found in `vault.txt`. Load PDF first.")
        return None, None

    with open(VAULT_FILE, "r", encoding="utf-8") as vault:
        vault_content = vault.readlines()

    vault_embeddings = []
    for line in vault_content:
        if line.strip():
            embedding = ollama.embeddings(model='llama3.2:1b', prompt=line)["embedding"]
            vault_embeddings.append(embedding)

    if not vault_embeddings:
        st.error("🚨 Error: No valid text extracted for embeddings.")
        return None, None

    vault_embeddings_tensor = torch.tensor(vault_embeddings, dtype=torch.float32)

    return vault_embeddings_tensor, vault_content

# ✅ Retrieve Relevant Context
def get_relevant_context(user_input, vault_embeddings, vault_content, top_k=3):
    if vault_embeddings is None:
        return "No context available."

    input_embedding = ollama.embeddings(model='llama3.2:1b', prompt=user_input)["embedding"]
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    top_indices = torch.topk(cos_scores, k=min(top_k, len(cos_scores)))[1].tolist()
    relevant_context = "\n".join(vault_content[idx].strip() for idx in top_indices)

    return relevant_context

# ✅ Chat Function with RAG + Debugging
def ollama_chat(user_input, vault_embeddings, vault_content):
    st.text_area("🛠 Debugging - User Input:", user_input)  # Debugging user input
    context = get_relevant_context(user_input, vault_embeddings, vault_content)
    query_with_context = f"Relevant Context:\n{context}\n\nUser Query: {user_input}"

    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "system", "content": query_with_context}]
        )

        # ✅ Clean unwanted tokens from the response
        cleaned_response = re.sub(r"<\|.*?\|>", "", response["message"]["content"]).strip()

        st.text_area("🛠 Debugging - API Response:", cleaned_response)  # Debugging API response
        return cleaned_response

    except Exception as e:
        st.error(f"🚨 Error communicating with Ollama: {e}")
        return f"Error: {e}"

# ✅ Streamlit Chat Interface
def show_chat():
    st.title("💬 AI ChatBot (RAG + Ollama 3.2)")

    if "vault_loaded" not in st.session_state:
        load_pdf()
        st.session_state.vault_loaded = True

    vault_embeddings, vault_content = generate_embeddings()

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    # ✅ Debugging Session State
    st.text_area("🛠 Debugging - Session State:", str(st.session_state))

    # ✅ Styling for Chat Messages
    st.markdown(
        """
        <style>
            .chat-container {
                background-color: #f8f9fa; 
                padding: 10px; 
                border-radius: 8px; 
                margin-bottom: 10px;
                color: black;
                max-width: 100%;
            }
            .user-msg {
                background-color: #d3e3fc;
                padding: 10px;
                border-radius: 8px;
                color: black;
                align-self: flex-end;
            }
            .bot-msg {
                background-color: #c3c3c3;
                padding: 10px;
                border-radius: 8px;
                color: black;
                align-self: flex-start;
            }
            .chat-wrapper {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ✅ Render chat messages
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
    for msg in st.session_state['messages']:
        if msg["role"] == "User":
            st.markdown(f'<div class="chat-container user-msg"><strong>User:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-container bot-msg"><strong>Bot:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ✅ Ensure chat input state is initialized
    if "chat_input" not in st.session_state:
        st.session_state["chat_input"] = ""

    # ✅ Function to process user input safely
    def process_message():
        user_message = st.session_state["chat_input"].strip()

        if user_message:
            st.session_state['messages'].append({"role": "User", "content": user_message})
            bot_response = ollama_chat(user_message, vault_embeddings, vault_content)
            st.session_state['messages'].append({"role": "Bot", "content": bot_response})

            # ✅ Instead of modifying the key, reset it using session state workaround
            st.session_state["chat_input_temp"] = ""  
            st.rerun()  # Force UI update

    # ✅ Debugging Input State
    st.text_area("🛠 Debugging - Chat Input:", st.session_state.get("chat_input", ""))

    # ✅ User input field (avoid modifying `st.session_state.chat_input` directly)
    user_input = st.text_input("Type your message:", key="chat_input_temp", value="", on_change=process_message)

    # ✅ Buttons for sending message & resetting chat
    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("Send", key="send_btn"):
            process_message()

    with col2:
        if st.button("New Chat", key="clear_btn"):
            st.session_state['messages'] = []
            st.rerun()
