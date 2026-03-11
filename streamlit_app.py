import streamlit as st
import requests

st.set_page_config(page_title="AI Mental Wellness Support Bot", layout="centered")

st.title("AI Mental Wellness Support Bot")
st.write("Talk with the AI support bot about how you're feeling.")

FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/7b60721f-874f-4f0a-a811-ca1f43c0d1fd"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hey... I'm here. What's going on in your heart right now?"
        }
    ]

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("How are you feeling today?")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    payload = {
        "question": user_input
    }

    try:
        with st.spinner("Aanya is thinking..."):
            response = requests.post(FLOWISE_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            bot_reply = result.get("text") or result.get("answer") or "I'm here with you."

        else:
            bot_reply = "I'm having trouble connecting right now."

    except Exception:
        bot_reply = "Something went wrong while talking to the AI."

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
