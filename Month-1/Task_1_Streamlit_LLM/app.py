import streamlit as st
import requests
import json

# --- Page Setup ---
st.set_page_config(page_title="Ollama Local Chat", page_icon="💻", layout="wide")

# --- Custom CSS for Better UI ---

# --- Custom CSS for Better UI ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True) # Yahan 'unsafe_allow_html' hona chahiye
# --- Initialize Session State (History) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Sidebar for Controls ---
with st.sidebar:
    st.title("Settings")
    
    model_choice = st.text_input("Enter Ollama Model Name:", value="llama3:latest")
    # model_choice = st.text_input("Enter Ollama Model Name:", value="llama3")
    st.divider()
    if st.button("Reset Conversation", type="primary"):
        st.session_state.chat_history = []
        st.rerun()

# --- Main Interface ---
st.title("Local LLM Interface")
st.caption("Powered by Ollama & Streamlit")

# Display Chat History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Logic ---
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Ollama Local API
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            url = "http://localhost:11434/api/generate"
            payload = {
                "model": model_choice,
                "prompt": prompt,
                "stream": True  # Streaming for better UI experience
            }
            
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    token = chunk.get("response", "")
                    full_response += token
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            # Add assistant response to history
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error: {str(e)}. Make sure Ollama is running.")















