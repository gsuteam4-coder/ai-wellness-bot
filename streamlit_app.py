import streamlit as st
import requests
import uuid

st.set_page_config(page_title="AI Mental Wellness Diagnostic Bot", layout="centered")

FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/7b60721f-874f-4f0a-a811-ca1f43c0d1fd"

st.title("AI Mental Wellness Diagnostic Bot")
st.write("This demo uses one fixed patient persona.")

# Fixed patient persona
persona_name = "Alex"
persona_age = 22
persona_problem = "exam stress, overthinking, poor sleep"
persona_routine = "classes, part-time job, studies late, skips breakfast"

st.markdown("### Patient Persona")
st.write(f"**Name:** {persona_name}")
st.write(f"**Age:** {persona_age}")
st.write(f"**Main Problem:** {persona_problem}")
st.write(f"**Routine:** {persona_routine}")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "You are now interacting with Alex. Describe how Alex is feeling today."
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type Alex's response here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    persona_context = f"""
Patient Persona:
Name: {persona_name}
Age: {persona_age}
Main Problem: {persona_problem}
Routine: {persona_routine}

Current Message: {user_input}
"""

    payload = {
        "question": persona_context,
        "overrideConfig": {
            "sessionId": st.session_state.session_id
        }
    }

    try:
        response = requests.post(FLOWISE_URL, json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()
            bot_reply = (
                result.get("text") or
                result.get("answer") or
                result.get("output") or
                "No response generated."
            )
        else:
            bot_reply = f"Error {response.status_code}: {response.text}"

    except Exception as e:
        bot_reply = f"Connection error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
