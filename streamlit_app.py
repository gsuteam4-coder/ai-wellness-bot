import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Aanya - AI Companion", layout="centered")

FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/7b60721f-874f-4f0a-a811-ca1f43c0d1fd"

st.title("💚 Aanya - Your AI Companion")
st.write("Talk freely. Aanya is here to listen.")

# Restart button
if st.button("🔄 Restart Conversation"):
    st.session_state.clear()
    st.rerun()

# Session ID (for memory)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Chat history
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
    clean_input = user_input.strip()

    # Prevent empty input (fixes 500 error)
    if clean_input == "":
        st.stop()

    st.session_state.messages.append({"role": "user", "content": clean_input})

    with st.chat_message("user"):
        st.markdown(clean_input)

    # Correct payload for Flowise
    payload = {
        "question": clean_input,
        "overrideConfig": {
            "sessionId": st.session_state.session_id
        }
    }

    try:
        response = requests.post(FLOWISE_URL, json=payload, timeout=60)

        if response.status_code == 200:
            data = response.json()

            # Handle different Flowise outputs safely
            if isinstance(data, dict):
                bot_reply = data.get("text") or data.get("answer") or data.get("output")
            else:
                bot_reply = str(data)

            if not bot_reply:
                bot_reply = "Hmm… I didn’t get that properly. Can you try again?"

        else:
            bot_reply = f"⚠️ Error {response.status_code}. Please try again."

    except Exception as e:
        bot_reply = f"⚠️ Connection error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
