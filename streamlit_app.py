import json
import re
import uuid
import streamlit as st
from flowise import Flowise, PredictionData

st.set_page_config(page_title="Aanya Wellness Simulation", layout="centered")

BASE_URL = "https://cloud.flowiseai.com"
FLOW_ID = "fd821f6f-939f-4b5c-89b4-910760fcb0f8"

st.title("💚 Aanya Wellness Simulation")
st.caption("Choose a path and see how the story unfolds.")

client = Flowise(base_url=BASE_URL)

def extract_options(text: str):
    pattern = r'^\s*([ABC])\)\s*(.+)$'
    return re.findall(pattern, text, flags=re.MULTILINE)

def is_final_result(text: str) -> bool:
    upper_text = text.upper()
    return "FINAL RESULT" in upper_text or "WELLNESS LEVEL" in upper_text

def stream_flowise(user_message: str, session_id: str):
    completion = client.create_prediction(
        PredictionData(
            chatflowId=FLOW_ID,
            question=user_message,
            overrideConfig={"sessionId": session_id},
            streaming=True
        )
    )

    for chunk in completion:
        try:
            parsed = json.loads(chunk)
            if parsed.get("event") == "token" and parsed.get("data"):
                yield str(parsed["data"])
        except Exception:
            continue

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "history" not in st.session_state:
    st.session_state.history = []

if "started" not in st.session_state:
    st.session_state.started = False

if st.button("🔄 Restart Simulation"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.history = []
    st.session_state.started = False
    st.rerun()

if not st.session_state.started:
    if st.button("▶ Start Simulation"):
        with st.spinner("Starting simulation..."):
            full_response = st.write_stream(
                stream_flowise("Start the simulation", st.session_state.session_id)
            )
        st.session_state.history.append(full_response)
        st.session_state.started = True
        st.rerun()

for item in st.session_state.history:
    st.markdown(item)
    st.divider()

if st.session_state.started and st.session_state.history:
    latest_output = st.session_state.history[-1]

    if not is_final_result(latest_output):
        options = extract_options(latest_output)

        if options:
            st.markdown("### Choose what happens next")

            cols = st.columns(len(options))

            for i, (letter, option_text) in enumerate(options):
                with cols[i]:
                    if st.button(
                        f"{letter}) {option_text}",
                        key=f"{letter}_{len(st.session_state.history)}"
                    ):
                        with st.spinner("Continuing story..."):
                            full_response = st.write_stream(
                                stream_flowise(letter, st.session_state.session_id)
                            )
                        st.session_state.history.append(full_response)
                        st.rerun()
        else:
            st.info("No options found in the latest response.")
