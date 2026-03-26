import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Aanya 💚")
st.write("Talk to someone who listens...")

# Session states
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

# Questions + options
flow = [
    ("How has your daily life been lately?", ["Busy", "Normal", "Very stressful"]),
    ("How has your sleep been lately?", ["Good", "Okay", "Bad"]),
    ("Are you eating okay these days?", ["Yes", "Sometimes skip", "Not really"]),
    ("How are things going with work or study?", ["Going well", "Struggling", "Overwhelmed"]),
    ("How are your relationships?", ["Good", "Okay", "Difficult"]),
    ("How has your mood been recently?", ["Happy", "Up and down", "Low"]),
    ("What do you do when things feel heavy?", ["Talk to someone", "Distract myself", "Nothing"])
]

# Show chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

step = st.session_state.step

# Show current question
if step < len(flow):
    question, options = flow[step]

    st.chat_message("assistant").write(
        f"That makes sense 💚\n{question}"
    )

    # Clickable options
    choice = st.radio("Choose one:", options, key=f"q{step}")

    if st.button("Next"):
        st.session_state.messages.append({"role": "user", "content": choice})
        st.session_state.step += 1
        st.rerun()

else:
    # Final result
    st.chat_message("assistant").write(
        "Result: Moderate\n\n"
        "• Try to get small breaks in your day\n"
        "• Talk to someone you trust\n"
        "• Keep a simple daily routine\n\n"
        "💚 I'm an AI companion, not a real therapist. Please reach out to a professional if things feel heavy."
    )
