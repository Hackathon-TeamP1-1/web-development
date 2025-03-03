import streamlit as st
import ollama
import PyPDF2
import os
import torch
import re
import pickle

# ✅ Define Constants
PDF_FILE = "details.pdf"
VAULT_FILE = "vault.txt"
EMBEDDINGS_CACHE = "embeddings_cache.pkl"

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

# ✅ Generate Embeddings for RAG (Caching Enabled)
def generate_embeddings():
    if os.path.exists(EMBEDDINGS_CACHE):
        with open(EMBEDDINGS_CACHE, "rb") as cache_file:
            return pickle.load(cache_file)

    if not os.path.exists(VAULT_FILE):
        return None, None

    with open(VAULT_FILE, "r", encoding="utf-8") as vault:
        vault_content = vault.readlines()

    vault_embeddings = []
    for line in vault_content:
        if line.strip():
            embedding = ollama.embeddings(model='llama3.2:1b', prompt=line)["embedding"]
            vault_embeddings.append(embedding)

    if not vault_embeddings:
        return None, None

    vault_embeddings_tensor = torch.tensor(vault_embeddings, dtype=torch.float32)

    with open(EMBEDDINGS_CACHE, "wb") as cache_file:
        pickle.dump((vault_embeddings_tensor, vault_content), cache_file)

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

# ✅ Chat Function with RAG
def ollama_chat(user_input, vault_embeddings, vault_content):
    context = get_relevant_context(user_input, vault_embeddings, vault_content)
    query_with_context = f"Relevant Context:\n{context}\n\nUser Query: {user_input}"

    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "system", "content": query_with_context}]
        )

        cleaned_response = re.sub(r"<\|.*?\|>", "", response["message"]["content"]).strip()

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

    if 'loading' not in st.session_state:
        st.session_state['loading'] = False

    # ✅ Render chat messages
    for msg in st.session_state['messages']:
        st.markdown(f"**{msg['role']}:** {msg['content']}")

    def process_message():
        user_message = st.session_state["chat_input"].strip()

        if user_message:
            st.session_state['messages'].append({"role": "User", "content": user_message})
            st.session_state['loading'] = True
            
            bot_response = ollama_chat(user_message, vault_embeddings, vault_content)
            st.session_state['messages'].append({"role": "Bot", "content": bot_response})
            st.session_state['loading'] = False
            
            # ✅ Use the correct rerun function
            st.session_state.pop("chat_input", None)  # Remove key safely
            st.rerun()  # ✅ Updated to avoid experimental_rerun error

    user_input = st.text_input(
        "Type your message:", 
        key="chat_input", 
        value=st.session_state.get("chat_input", ""),
        disabled=st.session_state['loading']
    )

    if st.session_state['loading']:
        with st.spinner("Thinking... 💭"):
            pass

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Send", disabled=st.session_state['loading']):
            process_message()
    with col2:
        if st.button("New Chat"):
            st.session_state['messages'] = []
            st.rerun()
