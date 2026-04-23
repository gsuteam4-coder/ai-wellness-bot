import json
import re
import uuid
import streamlit as st
from flowise import Flowise, PredictionData

st.set_page_config(page_title="The Resilience Game", layout="wide")

BASE_URL = "https://cloud.flowiseai.com"
FLOW_ID = "fd821f6f-939f-4b5c-89b4-910760fcb0f8"

client = Flowise(base_url=BASE_URL)

PERSONAS = {
    "Malik": {
        "title": "Malik — Social Anxiety",
        "summary": "Malik struggles with group events, overthinking, and fear of judgment.",
        "emoji": "🧑🏽",
    },
    "Rina": {
        "title": "Rina — Caregiver Burnout",
        "summary": "Rina is emotionally drained from always caring for others and neglecting herself.",
        "emoji": "👩🏽",
    },
    "Ava": {
        "title": "Ava — Chronic Pain",
        "summary": "Ava lives with ongoing pain, low energy, and frustration from not feeling understood.",
        "emoji": "👩🏼",
    }
}

st.markdown("""
<style>
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1120px;
}

.stApp {
    background: radial-gradient(circle at top left, #0d1b2a 0%, #07111f 45%, #040913 100%);
}

/* Header */
.hero-wrap {
    padding: 1.3rem 1.5rem;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(34,197,94,0.18), rgba(59,130,246,0.18));
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.4rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
}

.main-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.25rem;
    letter-spacing: -0.02em;
}

.sub-title {
    color: #bfc7d5;
    margin-bottom: 0;
    font-size: 1.02rem;
    line-height: 1.6;
}

/* Top action row */
.top-action {
    padding: 0.9rem 1rem;
    border-radius: 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 1.3rem;
}

/* Persona cards */
.persona-card {
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 22px;
    background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    min-height: 235px;
    transition: all 0.25s ease;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.persona-card:hover {
    transform: translateY(-4px);
    border-color: rgba(74,222,128,0.35);
    box-shadow: 0 14px 32px rgba(0,0,0,0.22);
}

.persona-emoji {
    font-size: 2.4rem;
    margin-bottom: 8px;
}

.persona-title {
    margin-top: 6px;
    margin-bottom: 10px;
    font-size: 1.85rem;
    font-weight: 700;
    line-height: 1.25;
}

.persona-summary {
    color: #b7c2d3;
    font-size: 0.98rem;
    line-height: 1.7;
}

/* Selected persona */
.selected-banner {
    padding: 16px 18px;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(80,200,120,0.13), rgba(59,130,246,0.10));
    border: 1px solid rgba(80,200,120,0.20);
    margin-bottom: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.12);
}

/* Story section */
.section-title {
    font-size: 1.55rem;
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 0.85rem;
}

.small-muted {
    color: #aeb7c7;
    font-size: 0.95rem;
}

.scene-box {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 24px;
    background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.02));
    margin-bottom: 18px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.15);
}

.final-box {
    border: 1px solid rgba(80,200,120,0.25);
    border-radius: 20px;
    padding: 24px;
    background: linear-gradient(180deg, rgba(80,200,120,0.08), rgba(80,200,120,0.04));
    margin-top: 16px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.16);
}

.scene-badge {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(80,200,120,0.18);
    color: #d6ffe2;
    font-weight: 700;
    margin-bottom: 14px;
    font-size: 0.92rem;
}

.aanya {
    border-left: 5px solid #4ade80;
    padding: 14px 16px;
    margin: 14px 0;
    background: rgba(74,222,128,0.08);
    border-radius: 14px;
    line-height: 1.7;
}

.persona {
    border-left: 5px solid #60a5fa;
    padding: 14px 16px;
    margin: 14px 0;
    background: rgba(96,165,250,0.08);
    border-radius: 14px;
    line-height: 1.7;
}

.insight-box {
    border-left: 4px solid #facc15;
    padding: 14px;
    margin: 16px 0;
    background: rgba(250,204,21,0.08);
    border-radius: 12px;
    line-height: 1.65;
}

/* Options */
.option-card {
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 18px;
    background: linear-gradient(180deg, rgba(255,255,255,0.035), rgba(255,255,255,0.02));
    min-height: 205px;
    margin-bottom: 12px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.12);
    transition: all 0.2s ease;
}

.option-card:hover {
    border-color: rgba(96,165,250,0.35);
    transform: translateY(-2px);
}

.option-label {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    font-size: 0.84rem;
    font-weight: 700;
    background: rgba(96,165,250,0.14);
    color: #dbeafe;
    margin-bottom: 10px;
}

.option-title {
    font-weight: 700;
    margin-bottom: 10px;
    font-size: 1rem;
}

.option-text {
    color: #b7c2d3;
    line-height: 1.65;
    font-size: 0.96rem;
}

/* Buttons */
div[data-testid="stButton"] > button {
    border-radius: 14px !important;
    min-height: 46px;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.10);
}

div[data-testid="stButton"] > button:hover {
    border-color: rgba(74,222,128,0.35);
}

/* Progress */
div[data-testid="stProgressBar"] > div {
    border-radius: 999px;
}

/* Divider space */
.story-gap {
    height: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-wrap">
    <div class="main-title">🌿 The Resilience Game</div>
    <div class="sub-title">
        Choose a persona and guide them through real-life emotional situations while exploring different paths of resilience.
    </div>
</div>
""", unsafe_allow_html=True)

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("**", "")
    text = text.replace("---", "")
    return text.strip()

def extract_options(text: str):
    text = clean_text(text)
    marker = "Choose what happens next:"
    idx = text.lower().find(marker.lower())
    if idx == -1:
        return []

    choice_part = text[idx + len(marker):].strip()

    match = re.search(
        r"A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*)",
        choice_part,
        flags=re.DOTALL | re.IGNORECASE
    )

    if not match:
        return []

    a_text = " ".join(match.group(1).split())
    b_text = " ".join(match.group(2).split())
    c_text = " ".join(match.group(3).split())

    c_text = re.split(
        r"Reflection Insight|FINAL RESULT|SCENE\s+\d+",
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
    text = clean_text(text)

    scene_match = re.search(r"SCENE\s+(\d+)", text, flags=re.IGNORECASE)
    if scene_match:
        scene_num = int(scene_match.group(1))
        st.markdown(f'<div class="scene-badge">🎬 Scene {scene_num} of 5</div>', unsafe_allow_html=True)
        st.progress(scene_num / 5)

    final = is_final_result(text)

    story_only = re.split(r"Choose what happens next:", text, maxsplit=1, flags=re.IGNORECASE)[0]
    lines = [line.strip() for line in story_only.splitlines() if line.strip()]

    box_class = "final-box" if final else "scene-box"
    st.markdown(f'<div class="{box_class}">', unsafe_allow_html=True)

    for line in lines:
        if line.lower().startswith("reflection insight"):
            insight = line.split(":", 1)[1].strip() if ":" in line else line
            st.markdown(
                f'<div class="insight-box">💡 <b>Reflection Insight</b><br>{insight}</div>',
                unsafe_allow_html=True
            )
        elif line.startswith("Aanya:"):
            content = line.replace("Aanya:", "", 1).strip()
            st.markdown(
                f'<div class="aanya"><b>Aanya 💚</b><br>{content}</div>',
                unsafe_allow_html=True
            )
        elif ":" in line and not line.upper().startswith("FINAL RESULT"):
            speaker, content = line.split(":", 1)
            speaker = speaker.strip()
            content = content.strip()
            st.markdown(
                f'<div class="persona"><b>{speaker}</b><br>{content}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"<p style='line-height:1.8; color:#e5ecf5;'>{line}</p>", unsafe_allow_html=True)

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
    st.markdown('<div class="top-action">', unsafe_allow_html=True)
    if st.button("🔄 Restart", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.started = False
        st.session_state.history = []
        st.session_state.selected_persona = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.selected_persona:
    st.markdown('<div class="section-title">Choose a persona</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    for col, key in zip([col1, col2, col3], ["Malik", "Rina", "Ava"]):
        p = PERSONAS[key]
        with col:
            st.markdown(
                f"""
                <div class="persona-card">
                    <div class="persona-emoji">{p['emoji']}</div>
                    <div class="persona-title">{p['title']}</div>
                    <div class="persona-summary">{p['summary']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"Choose {key}", key=f"choose_{key}", use_container_width=True):
                st.session_state.selected_persona = key
                st.rerun()

    st.stop()
else:
    p = PERSONAS[st.session_state.selected_persona]
    st.markdown(
        f"""
        <div class="selected-banner">
            <b>Selected persona:</b> {p['title']}<br>
            <span class="small-muted">{p['summary']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

if not st.session_state.started:
    st.markdown('<div class="section-title">Start the story</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-muted">Begin Scene 1 and let Aanya guide the emotional journey.</div>', unsafe_allow_html=True)

    if st.button("▶ Start Simulation", key="start_simulation", use_container_width=True):
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
    st.markdown("<div class='story-gap'></div>", unsafe_allow_html=True)

if st.session_state.history:
    latest = clean_text(st.session_state.history[-1])

    if not is_final_result(latest):
        options = extract_options(latest)

        if options:
            st.markdown('<div class="section-title">Choose your guidance</div>', unsafe_allow_html=True)
            st.markdown('<div class="small-muted">Each choice leads the story in a different emotional direction.</div>', unsafe_allow_html=True)

            cols = st.columns(3)

            for idx, (letter, option_text) in enumerate(options):
                with cols[idx]:
                    st.markdown(
                        f"""
                        <div class="option-card">
                            <div class="option-label">Option {letter}</div>
                            <div class="option-title">Your choice</div>
                            <div class="option-text">{option_text}</div>
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
