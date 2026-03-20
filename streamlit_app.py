import streamlit as st
import requests
import uuid

st.set_page_config(page_title="AI Mental Wellness Diagnostic Bot", layout="centered")

st.title("AI Mental Wellness Diagnostic Bot")
st.write("Choose a persona and interact with the AI diagnostic system.")

FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/7b60721f-874f-4f0a-a811-ca1f43c0d1fd"

# Personas
personas = {
    "Alex – College Student with Anxiety": {
        "age": 22,
        "problem": "exam stress, overthinking, poor sleep",
        "routine": "classes, part-time job, studies late, skips breakfast"
    },
    "Maya – Working Professional with Burnout": {
        "age": 29,
        "problem": "burnout, exhaustion, emotional overload",
        "routine": "long office hours, constant meetings, little rest"
    },
    "Ravi – Remote Worker with Loneliness": {
        "age": 26,
        "problem": "isolation, low motivation, disconnected feeling",
        "routine": "works from home, little social contact, irregular sleep"
    },
    "Sara – Entrepreneur with Sleep Stress": {
        "age": 31,
        "problem": "stress, insomnia, constant pressure",
        "routine": "late-night work, high caffeine, always thinking about business"
    }
}

# Persona selection
selected_persona = st.selectbox("Choose a persona", list(personas.keys()))
persona_info = personas[selected_persona]

# Show persona details
st.markdown("### Persona Details")
st.write(f"**Age:** {persona_info['age']}")
st.write(f"**Main Problem:** {persona_info['problem']}")
st.write(f"**Routine:** {persona_info['routine']}")

# Session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Chat history reset when persona changes
if "current_persona" not in st.session_state:
    st.session_state.current_persona = selected_persona
    st.session_state.messages = []

if selected_persona != st.session_state.current_persona:
    st.session_state.current_persona = selected_persona
    st.session_state.messages = []

# Initial message
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"You are now interacting with {selected_persona}. Describe how you feel today."
    })

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Type your response here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Persona context
    persona_context = f"""
Persona: {selected_persona}
Age: {persona_info['age']}
Main problem: {persona_info['problem']}
Routine: {persona_info['routine']}

User says: {user_input}
"""

    payload = {
        "question": persona_context,
        "overrideConfig": {
            "sessionId": st.session_state.session_id
        }
    }

    try:
        response = requests.post(FLOWISE_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            bot_reply = result.get("text", "No response generated.")
        else:
            bot_reply = f"Error: {response.status_code}"

    except Exception as e:
        bot_reply = f"Connection error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
