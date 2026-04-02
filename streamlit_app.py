import json
import re
import uuid
import streamlit as st
from flowise import Flowise, PredictionData

st.set_page_config(page_title="Aanya Wellness Simulation", layout="wide")

BASE_URL = "https://cloud.flowiseai.com"
FLOW_ID = "fd821f6f-939f-4b5c-89b4-910760fcb0f8"

client = Flowise(base_url=BASE_URL)

PERSONAS = {
    "Malik": {
        "title": "Malik — Social Anxiety",
        "summary": "Malik struggles with group events, overthinking, and fear of judgment.",
        "emoji": "🧑🏽",
        "color": "#1f6f8b"
    },
    "Rina": {
        "title": "Rina — Caregiver Burnout",
        "summary": "Rina is emotionally drained from always caring for others and neglecting herself.",
        "emoji": "👩🏽",
        "color": "#7b4f9c"
    },
    "Ava": {
        "title": "Ava — Chronic Pain",
        "summary": "Ava lives with ongoing pain, low energy, and frustration from not feeling understood.",
        "emoji": "👩🏼",
        "color": "#9c6b30"
    }
}

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}
.main-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}
.sub-title {
    color: #bfc7d5;
    margin-bottom: 1.5rem;
}
.persona-card {
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 20px;
    background: rgba(255,255,255,0.03);
    min-height: 220px;
}
.scene-box {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 24px;
    background: rgba(255,255,255,0.02);
    margin-bottom: 18px;
}
.choice-box {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px;
    background: rgba(255,255,255,0.02);
    margin-top: 12px;
}
.final-box {
    border: 1px solid rgba(80,200,120,0.25);
    border-radius: 18px;
    padding: 24px;
    background: rgba(80,200,120,0.06);
    margin-top: 16px;
}
.round-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(80,200,120,0.18);
    color: #d6ffe2;
    font-weight: 700;
    margin-bottom: 12px;
}
.aanya {
    border-left: 5px solid #4ade80;
    padding: 12px 16px;
    margin: 12px 0;
    background: rgba(74,222,128,0.08);
    border-radius: 12px;
}
.persona {
    border-left: 5px solid #60a5fa;
    padding: 12px 16px;
    margin: 12px 0;
    background: rgba(96,165,250,0.08);
    border-radius: 12px;
}
.section-title {
    font-size: 1.6rem;
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 0.8rem;
}
.small-muted {
    color: #aeb7c7;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💚 Aanya Wellness Simulation</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Choose a persona and explore their emotional journey through guided decisions.</div>', unsafe_allow_html=True)


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


def render_story_block(text: str):
    text = normalize_text(text)

    round_match = re.search(r"ROUND\s+(\d+)", text, flags=re.IGNORECASE)
    if round_match:
        round_num = int(round_match.group(1))
        st.markdown(f'<div class="round-badge">Round {round_num}</div>', unsafe_allow_html=True)
        st.progress(round_num / 4)

    final = is_final_result(text)

    lines = text.splitlines()
    choices_started = False

    scene_lines = []
    choice_lines = []

    for line in lines:
        clean = line.strip()
        if not clean:
            continue

        if clean.lower().startswith("choose what happens next"):
            choices_started = True
            continue

        if choices_started:
            choice_lines.append(clean)
        else:
            scene_lines.append(clean)

    box_class = "final-box" if final else "scene-box"
    st.markdown(f'<div class="{box_class}">', unsafe_allow_html=True)

    for line in scene_lines:
        if line.startswith("Aanya:"):
            content = line.replace("Aanya:", "", 1).strip()
            st.markdown(f'<div class="aanya"><b>Aanya 💚</b><br>{content}</div>', unsafe_allow_html=True)
        elif ":" in line and not line.upper().startswith("FINAL RESULT"):
            speaker, content = line.split(":", 1)
            speaker = speaker.strip()
            content = content.strip()
            st.markdown(f'<div class="persona"><b>{speaker}</b><br>{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"<p>{line}</p>", unsafe_allow_html=True)

    if choice_lines and not final:
        st.markdown('<div class="choice-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">✨ What would you do in this moment?</div>', unsafe_allow_html=True)
        for line in choice_lines:
            st.markdown(f"<p>{line}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "started" not in st.session_state:
    st.session_state.started = False
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = None


top_col1, top_col2 = st.columns([1, 5])
with top_col1:
    if st.button("🔄 Restart"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.started = False
        st.session_state.history = []
        st.session_state.selected_persona = None
        st.rerun()

if not st.session_state.selected_persona:
    st.markdown('<div class="section-title">Choose a persona</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    for col, key in zip([col1, col2, col3], ["Malik", "Rina", "Ava"]):
        p = PERSONAS[key]
        with col:
            st.markdown(
                f"""
                <div class="persona-card">
                    <div style="font-size:2rem;">{p['emoji']}</div>
                    <h3 style="margin-top:8px;">{p['title']}</h3>
                    <p class="small-muted">{p['summary']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"Choose {key}", use_container_width=True):
                st.session_state.selected_persona = key
                st.rerun()

    st.stop()
else:
    p = PERSONAS[st.session_state.selected_persona]
    st.markdown(
        f"""
        <div style="padding:14px 18px; border-radius:14px; background:rgba(80,200,120,0.12); margin-bottom:18px;">
            <b>Selected persona:</b> {p['title']}
        </div>
        """,
        unsafe_allow_html=True
    )

if not st.session_state.started:
    if st.button("▶ Start Simulation", use_container_width=True):
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

for item in st.session_state.history:
    render_story_block(item)
    st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.history:
    latest = st.session_state.history[-1]

    if not is_final_result(latest):
        options = extract_options(latest)

        if options:
            st.markdown('<div class="section-title">Choose your guidance</div>', unsafe_allow_html=True)
            cols = st.columns(3)

            for idx, (letter, option_text) in enumerate(options):
                with cols[idx]:
                    st.markdown(
                        f"""
                        <div class="persona-card" style="min-height:180px;">
                            <div style="font-weight:700; margin-bottom:8px;">Option {letter}</div>
                            <div class="small-muted">{option_text}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if st.button(
                        f"Select {letter}",
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
            with st.expander("Debug latest response"):
                st.code(latest)
