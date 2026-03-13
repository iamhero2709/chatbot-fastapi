import os
import streamlit as st
import requests

# Allow configuring the backend URL via environment variable
FASTAPI_URL = os.getenv("FASTAPI_URL", "https://chatbot-fastapi-production-b063.up.railway.app/api/chat")

st.set_page_config(page_title="Product Landing Page Bot", page_icon="🤖")

st.title("🌟 Welcome to Our Product!")
st.write("I am Nova, your virtual assistant. Feel free to ask me anything about what we do!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick-reply options to surface on the landing page
QUICK_REPLY_OPTIONS = [
    "What are your pricing plans?",
    "How does the product work?",
    "Can I see a demo?",
    "How can I contact sales?",
]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def call_backend(prompt: str, timeout: float = 10.0) -> str:
    try:
        response = requests.post(FASTAPI_URL, json={"user_message": prompt}, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            return data.get("reply", "(no reply returned)")
        elif response.status_code == 400:
            return "Your message looks empty or invalid. Please try again."
        elif response.status_code == 503:
            return "Backend is not ready; please try again shortly."
        else:
            return "Oops! Something went wrong on the server."
    except requests.exceptions.ConnectionError:
        return "Apologies, the backend server is currently unavailable. Please make sure the FastAPI server is running."
    except requests.exceptions.Timeout:
        return "The request timed out. Please try again."
    except Exception:
        return "Unexpected error when contacting the backend."


# React to user input
def send_message(prompt: str):
    """Helper to send a prompt to the backend and display the conversation in the UI."""
    if not prompt or not prompt.strip():
        return

    # Display user message and store in history
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call backend and display reply
    bot_reply = call_backend(prompt)
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})


# Render quick-reply buttons (horizontal)
cols = st.columns(len(QUICK_REPLY_OPTIONS))
for i, option in enumerate(QUICK_REPLY_OPTIONS):
    if cols[i].button(option):
        send_message(option)


# Chat input area (allows free text)
if prompt := st.chat_input("Hi! How can I help you today?"):
    send_message(prompt)
