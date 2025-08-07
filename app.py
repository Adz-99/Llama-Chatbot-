import os
import json

import streamlit as st
from groq import Groq

st.set_page_config(page_title="Llama 3.3 Chatbot", 
                   page_icon=":llama:",
                   layout="centered")

working_dir = os.path.dirname(os.path.abspath(__file__))
json_data = json.load(open(os.path.join(working_dir, "config.json")))

os.environ["GROQ_API_KEY"] = json_data["GROQ_API_KEY"]

client = Groq()

with st.sidebar:
    selected = st.selectbox("Select a model to chat with", options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
                             index=0, help="70B is more powerful but slower. 8B is faster for casual use.")

# Initialise chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🦙 Llama 3.3 Chatbot")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me anything...")

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Placeholder for the assistant's message
    with st.chat_message("assistant"):
        assistant_placeholder = st.empty()
        full_response = ""

        # Streaming response
        response = client.chat.completions.create(
            model=selected,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                *st.session_state.chat_history
            ],
            max_tokens=1000,
            temperature=0.7,
            stream=True,  # <-- Enable streaming
        )

        for chunk in response:
            delta = chunk.choices[0].delta.content or ""
            full_response += delta
            assistant_placeholder.markdown(full_response)

    # Add final response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})
