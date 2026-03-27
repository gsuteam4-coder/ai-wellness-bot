import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Aanya - AI Companion", layout="centered")

FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/7b60721f-874f-4f0a-a811-ca1f43c0d1fd"

st.title("💚 Aanya - Your AI Companion")
st.caption("Talk freely. Aanya is here to listen.")

# Restart button
if st.button("🔄 Restart Conversation"):
    st.session_state.clear()
    st.rerun()

# Session ID for memory
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hey… I'm here with you 😊 What's been on your mind lately?"
        }
    ]

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type how you're feeling...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    payload = {
        "question": user_input.strip(),
        "overrideConfig": {
            "sessionId": st.session_state.session_id
        }
    }

    try:
        response = requests.post(FLOWISE_URL, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            bot_reply = (
                result.get("text")
                or result.get("answer")
                or result.get("output")
                or "Hmm… something feels off. Can you try again?"
            )
        else:
            bot_reply = f"Something went wrong ({response.status_code})."
    except Exception:
        bot_reply = "I couldn't reach the server… try again in a moment 💚"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
