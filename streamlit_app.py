import json
import re
import uuid
import streamlit as st
from flowise import Flowise, PredictionData

st.set_page_config(page_title="Aanya Wellness Simulation", layout="centered")

BASE_URL = "https://cloud.flowiseai.com"
FLOW_ID = "fd821f6f-939f-4b5c-89b4-910760fcb0f8"

st.title("💚 Aanya Wellness Simulation")
st.caption("Choose a persona and explore their story.")

client = Flowise(base_url=BASE_URL)

PERSONAS = {
    "Malik": {
        "title": "Malik — Social Anxiety",
        "summary": "Malik struggles with group events, overthinking, and fear of judgment."
    },
    "Rina": {
        "title": "Rina — Caregiver Burnout",
        "summary": "Rina is emotionally drained from always caring for others and neglecting herself."
    },
    "Ava": {
        "title": "Ava — Chronic Pain",
        "summary": "Ava lives with ongoing pain, low energy, and frustration from not feeling understood."
    }
}


def normalize_text(text: str) -> str:
    if not text:
        return ""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def extract_options(text: str):
    text = normalize_text(text)

    marker = "Choose what happens next:"
    idx = text.lower().find(marker.lower())
    if idx == -1:
        return []

    choice_part = text[idx + len(marker):].strip()

    block_match = re.search(
        r"A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*)",
        choice_part,
        flags=re.DOTALL | re.IGNORECASE
    )

    if block_match:
        a_text = " ".join(block_match.group(1).split())
        b_text = " ".join(block_match.group(2).split())
        c_text = " ".join(block_match.group(3).split())

        c_text = re.split(
            r"FINAL RESULT|ROUND\s+\d+",
            c_text,
            maxsplit=1,
            flags=re.IGNORECASE
        )[0].strip()

        c_text = " ".join(c_text.split())

        if a_text and b_text and c_text:
            return [("A", a_text), ("B", b_text), ("C", c_text)]

    options = []
    for line in choice_part.splitlines():
        clean = line.strip()
        m = re.match(r"^([ABC])[\)\.\:\-]\s*(.+)$", clean, flags=re.IGNORECASE)
        if m:
            options.append((m.group(1).upper(), m.group(2).strip()))

    if len(options) == 3:
        return options

    return []


def is_final_result(text: str) -> bool:
    upper = text.upper()
    return "FINAL RESULT" in upper or "WELLNESS LEVEL" in upper


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

if "started" not in st.session_state:
    st.session_state.started = False

if "history" not in st.session_state:
    st.session_state.history = []

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = None


if st.button("🔄 Restart Simulation"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.started = False
    st.session_state.history = []
    st.session_state.selected_persona = None
    st.rerun()


if not st.session_state.selected_persona:
    st.markdown("## Choose a persona")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"### {PERSONAS['Malik']['title']}")
        st.write(PERSONAS["Malik"]["summary"])
        if st.button("Choose Malik"):
            st.session_state.selected_persona = "Malik"
            st.rerun()

    with col2:
        st.markdown(f"### {PERSONAS['Rina']['title']}")
        st.write(PERSONAS["Rina"]["summary"])
        if st.button("Choose Rina"):
            st.session_state.selected_persona = "Rina"
            st.rerun()

    with col3:
        st.markdown(f"### {PERSONAS['Ava']['title']}")
        st.write(PERSONAS["Ava"]["summary"])
        if st.button("Choose Ava"):
            st.session_state.selected_persona = "Ava"
            st.rerun()

    st.stop()
else:
    st.success(f"Selected persona: {PERSONAS[st.session_state.selected_persona]['title']}")


if not st.session_state.started:
    if st.button("▶ Start Simulation"):
        start_prompt = (
            f"Start the simulation for persona: {st.session_state.selected_persona}. "
            f"Persona summary: {PERSONAS[st.session_state.selected_persona]['summary']}"
        )

        with st.spinner("Starting simulation..."):
            full_response = st.write_stream(
                stream_flowise(start_prompt, st.session_state.session_id)
            )

        st.session_state.history.append(full_response)
        st.session_state.started = True
        st.rerun()


for idx, item in enumerate(st.session_state.history):
    round_match = re.search(r"ROUND\s+(\d+)", item, flags=re.IGNORECASE)
    if round_match:
        round_num = int(round_match.group(1))
        st.markdown(f"## 🟢 Round {round_num}")
        st.progress(round_num / 4)

    if "FINAL RESULT" in item.upper():
        st.markdown("## 🌟 Final Reflection")

    st.markdown(item)
    st.divider()


if st.session_state.history:
    latest = st.session_state.history[-1]

    if not is_final_result(latest):
        options = extract_options(latest)

        if options:
            st.markdown("### ✨ What would you do in this moment?")

            cols = st.columns(3)

            for idx, (letter, option_text) in enumerate(options):
                with cols[idx]:
                    st.markdown(f"**Option {letter}**")
                    if st.button(
                        option_text,
                        key=f"{letter}_{len(st.session_state.history)}",
                        use_container_width=True
                    ):
                        with st.spinner("Continuing story..."):
                            full_response = st.write_stream(
                                stream_flowise(letter, st.session_state.session_id)
                            )
                        st.session_state.history.append(full_response)
                        st.rerun()
        else:
            st.warning("Options were not found in the latest response.")
            with st.expander("Debug latest response"):
                st.code(latest)
