import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Aanya Wellness Simulation", layout="centered")

# NEW Flowise agent/chatflow URL
FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/fd821f6f-939f-4b5c-89b4-910760fcb0f8"

st.title("💚 Aanya Wellness Simulation")
st.caption("Choose a path and see how the story unfolds.")

# Restart simulation
if st.button("🔄 Restart Simulation"):
    st.session_state.clear()
    st.rerun()

# Session id for memory
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Conversation history
if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.started = False

# Start button
if not st.session_state.started:
    if st.button("▶ Start Simulation"):
        payload = {
            "question": "Start the simulation",
            "overrideConfig": {
                "sessionId": st.session_state.session_id
            }
        }

        try:
            response = requests.post(FLOWISE_URL, json=payload, timeout=60)

            if response.status_code == 200:
                result = response.json()
                output = (
                    result.get("text")
                    or result.get("answer")
                    or result.get("output")
                    or "No response generated."
                )
            else:
                output = f"Error {response.status_code}: {response.text}"

        except Exception as e:
            output = f"Connection error: {e}"

        st.session_state.history.append(output)
        st.session_state.started = True
        st.rerun()

# Show simulation history
for msg in st.session_state.history:
    st.markdown(msg)

# Choice buttons
if st.session_state.started:
    st.markdown("### Choose what happens next")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("A"):
            payload = {
                "question": "A",
                "overrideConfig": {
                    "sessionId": st.session_state.session_id
                }
            }

            try:
                response = requests.post(FLOWISE_URL, json=payload, timeout=60)

                if response.status_code == 200:
                    result = response.json()
                    output = (
                        result.get("text")
                        or result.get("answer")
                        or result.get("output")
                        or "No response generated."
                    )
                else:
                    output = f"Error {response.status_code}: {response.text}"

            except Exception as e:
                output = f"Connection error: {e}"

            st.session_state.history.append(output)
            st.rerun()

    with col2:
        if st.button("B"):
            payload = {
                "question": "B",
                "overrideConfig": {
                    "sessionId": st.session_state.session_id
                }
            }

            try:
                response = requests.post(FLOWISE_URL, json=payload, timeout=60)

                if response.status_code == 200:
                    result = response.json()
                    output = (
                        result.get("text")
                        or result.get("answer")
                        or result.get("output")
                        or "No response generated."
                    )
                else:
                    output = f"Error {response.status_code}: {response.text}"

            except Exception as e:
                output = f"Connection error: {e}"

            st.session_state.history.append(output)
            st.rerun()

    with col3:
        if st.button("C"):
            payload = {
                "question": "C",
                "overrideConfig": {
                    "sessionId": st.session_state.session_id
                }
            }

            try:
                response = requests.post(FLOWISE_URL, json=payload, timeout=60)

                if response.status_code == 200:
                    result = response.json()
                    output = (
                        result.get("text")
                        or result.get("answer")
                        or result.get("output")
                        or "No response generated."
                    )
                else:
                    output = f"Error {response.status_code}: {response.text}"

            except Exception as e:
                output = f"Connection error: {e}"

            st.session_state.history.append(output)
            st.rerun()
