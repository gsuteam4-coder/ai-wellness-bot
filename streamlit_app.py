import streamlit as st
import requests
import uuid

st.set_page_config(page_title="AI Mental Wellness Diagnostic Bot", layout="centered")

st.title("AI Mental Wellness Diagnostic Bot")
st.write("Talk with the AI diagnostic bot about your mental wellness.")

FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/7b60721f-874f-4f0a-a811-ca1f43c0d1fd"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hey, I’m here. Let’s understand what you’re going through, one step at a time."
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    payload = {
        "question": user_input,
        "overrideConfig": {
            "sessionId": st.session_state.session_id
        }
    }

    try:
        response = requests.post(FLOWISE_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            bot_reply = result.get("text", "I’m sorry, I could not generate a response.")
        else:
            bot_reply = f"Error connecting to AI bot. Status code: {response.status_code}"
    except Exception as e:
        bot_reply = f"Something went wrong: {e}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
