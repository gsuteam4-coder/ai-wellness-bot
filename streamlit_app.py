import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import tempfile

st.set_page_config(page_title="AI Mental Wellness Support Bot")

st.title("Aanya — Your Support Companion")

FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/7b60721f-874f-4f0a-a811-ca1f43c0d1fd"

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey... I'm here. What's on your mind today?"}
    ]

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# TEXT INPUT
user_input = st.chat_input("Type your message here...")

# MICROPHONE INPUT
st.write("Or speak to Aanya")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    just_once=True
)

# If voice recorded
if audio:
    st.audio(audio["bytes"])

# Process text input
if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    payload = {"question": user_input}

    try:
        with st.spinner("Aanya is thinking..."):
            response = requests.post(FLOWISE_URL, json=payload)

        result = response.json()
        bot_reply = result.get("text") or result.get("answer")

    except:
        bot_reply = "Something went wrong."

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.write(bot_reply)

    # TEXT → SPEECH
    tts = gTTS(bot_reply)

    audio_file = tempfile.NamedTemporaryFile(delete=False)
    tts.save(audio_file.name)

    st.audio(audio_file.name)
