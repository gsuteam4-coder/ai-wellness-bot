import streamlit as st
import requests
import re
import json

st.set_page_config(
    page_title="The Resilience Game",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# FLOWISE CONFIG
# -----------------------------
FLOWISE_API_URL = "https://cloud.flowiseai.com/api/v1/prediction/fd821f6f-939f-4b5c-89b4-910760fcb0f8"

PERSONAS = {
    "Malik": {
        "subtitle": "Social Anxiety",
        "emoji": "😟",
        "color": "linear-gradient(135deg, #60a5fa, #2563eb)",
        "description": "Malik often feels overwhelmed in social situations and struggles with fear of judgment."
    },
    "Rina": {
        "subtitle": "Caregiver Burnout",
        "emoji": "😔",
        "color": "linear-gradient(135deg, #f59e0b, #ea580c)",
        "description": "Rina is exhausted from caring for others and rarely gives herself time to rest."
    },
    "Ava": {
        "subtitle": "Chronic Pain",
        "emoji": "🌧️",
        "color": "linear-gradient(135deg, #a78bfa, #7c3aed)",
        "description": "Ava is managing daily pain while trying to hold on to routines, hope, and self-worth."
    }
}

# -----------------------------
# SESSION STATE
# -----------------------------
if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = None

if "story_started" not in st.session_state:
    st.session_state.story_started = False

if "current_scene" not in st.session_state:
    st.session_state.current_scene = 0

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if "final_result" not in st.session_state:
    st.session_state.final_result = False

if "raw_response" not in st.session_state:
    st.session_state.raw_response = ""

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        color: white;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    .hero-box {
        background: linear-gradient(135deg, #10b981, #2563eb);
        padding: 1.4rem 1.6rem;
        border-radius: 24px;
        margin-bottom: 1.2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #ecfeff;
    }

    .game-box {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 22px;
        padding: 1.2rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.20);
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.8rem;
    }

    .persona-card {
        border-radius: 20px;
        padding: 1rem;
        min-height: 220px;
        color: white;
        box-shadow: 0 8px 24px rgba(0,0,0,0.20);
        border: 1px solid rgba(255,255,255,0.15);
    }

    .persona-emoji {
        font-size: 2.8rem;
        margin-bottom: 0.4rem;
    }

    .persona-name {
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 0.15rem;
    }

    .persona-subtitle {
        font-size: 0.95rem;
        color: #f3f4f6;
        margin-bottom: 0.8rem;
    }

    .persona-desc {
        font-size: 0.92rem;
        line-height: 1.5;
        color: #f9fafb;
    }

    .story-panel {
        background: linear-gradient(180deg, #1f2937, #111827);
        border-radius: 22px;
        padding: 1.2rem;
        min-height: 420px;
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 8px 24px rgba(0,0,0,0.20);
    }

    .scene-badge {
        display: inline-block;
        background: #10b981;
        color: white;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-size: 0.86rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }

    .story-text {
        background: rgba(255,255,255,0.05);
        padding: 1rem;
        border-radius: 16px;
        color: #f3f4f6;
        line-height: 1.75;
        white-space: pre-wrap;
        min-height: 240px;
        font-size: 1rem;
    }

    .reflection-box {
        margin-top: 1rem;
        background: rgba(16,185,129,0.10);
        border: 1px solid rgba(16,185,129,0.30);
        border-radius: 16px;
        padding: 0.9rem 1rem;
        color: #d1fae5;
    }

    .tip-box {
        margin-top: 1rem;
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 1rem;
        color: #e5e7eb;
    }

    .footer-note {
        text-align: center;
        color: #9ca3af;
        font-size: 0.9rem;
        margin-top: 1rem;
    }

    div[data-testid="stButton"] > button {
        border-radius: 14px !important;
        min-height: 52px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HELPERS
# -----------------------------
def extract_text_from_response(data):
    if isinstance(data, str):
        return data.strip()

    if isinstance(data, dict):
        possible_keys = [
            "text", "response", "message", "answer", "output",
            "result", "content"
        ]
        for key in possible_keys:
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

        # nested structures
        for value in data.values():
            if isinstance(value, str) and value.strip():
                return value.strip()
            if isinstance(value, dict):
                nested = extract_text_from_response(value)
                if nested:
                    return nested
            if isinstance(value, list) and value:
                for item in value:
                    nested = extract_text_from_response(item)
                    if nested:
                        return nested

    if isinstance(data, list):
        for item in data:
            nested = extract_text_from_response(item)
            if nested:
                return nested

    return ""

def call_flowise(user_message: str) -> str:
    try:
        payload = {"question": user_message}

        response = requests.post(
            FLOWISE_API_URL,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        try:
            data = response.json()
            st.session_state.raw_response = json.dumps(data, indent=2)
        except Exception:
            data = response.text
            st.session_state.raw_response = str(data)

        text = extract_text_from_response(data)

        if not text:
            return "No story text was returned from Flowise. Check the raw response below."

        return text

    except Exception as e:
        st.session_state.raw_response = f"Request failed: {e}"
        return f"Error connecting to Flowise: {e}"

def extract_scene_number(text: str) -> int:
    match = re.search(r"SCENE\s+(\d+)", text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    if "FINAL RESULT" in text.upper():
        return 5
    return st.session_state.current_scene or 1

def extract_reflection(text: str) -> str:
    match = re.search(r"Reflection Insight:\s*(.*)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def parse_choices(text: str):
    pattern = r"A\)\s*(.*?)\nB\)\s*(.*?)\nC\)\s*(.*?)(?:\nReflection Insight:|$)"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return [
            match.group(1).strip(),
            match.group(2).strip(),
            match.group(3).strip()
        ]
    return []

def start_game(persona_name: str):
    st.session_state.selected_persona = persona_name
    st.session_state.story_started = True
    st.session_state.current_scene = 1
    st.session_state.final_result = False

    opening_prompt = f"Start with {persona_name}"
    response = call_flowise(opening_prompt)
    st.session_state.last_response = response

    if "FINAL RESULT" in response.upper():
        st.session_state.final_result = True
        st.session_state.current_scene = 5
    else:
        st.session_state.current_scene = extract_scene_number(response)

def send_choice(choice_text: str):
    response = call_flowise(choice_text)
    st.session_state.last_response = response

    if "FINAL RESULT" in response.upper():
        st.session_state.final_result = True
        st.session_state.current_scene = 5
    else:
        st.session_state.current_scene = extract_scene_number(response)

def restart_game():
    st.session_state.selected_persona = None
    st.session_state.story_started = False
    st.session_state.current_scene = 0
    st.session_state.last_response = ""
    st.session_state.final_result = False
    st.session_state.raw_response = ""

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">💚 The Resilience Game</div>
    <div class="hero-subtitle">
        Guide a wellness story. Support one persona through 5 scenes of emotional decisions, reflection, and growth.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# START SCREEN
# -----------------------------
if not st.session_state.story_started:
    st.markdown('<div class="game-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Choose a Persona to Begin</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        p = PERSONAS["Malik"]
        st.markdown(f"""
        <div class="persona-card" style="background:{p['color']};">
            <div class="persona-emoji">{p['emoji']}</div>
            <div class="persona-name">Malik</div>
            <div class="persona-subtitle">{p['subtitle']}</div>
            <div class="persona-desc">{p['description']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Malik's Story", use_container_width=True):
            start_game("Malik")
            st.rerun()

    with col2:
        p = PERSONAS["Rina"]
        st.markdown(f"""
        <div class="persona-card" style="background:{p['color']};">
            <div class="persona-emoji">{p['emoji']}</div>
            <div class="persona-name">Rina</div>
            <div class="persona-subtitle">{p['subtitle']}</div>
            <div class="persona-desc">{p['description']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Rina's Story", use_container_width=True):
            start_game("Rina")
            st.rerun()

    with col3:
        p = PERSONAS["Ava"]
        st.markdown(f"""
        <div class="persona-card" style="background:{p['color']};">
            <div class="persona-emoji">{p['emoji']}</div>
            <div class="persona-name">Ava</div>
            <div class="persona-subtitle">{p['subtitle']}</div>
            <div class="persona-desc">{p['description']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Ava's Story", use_container_width=True):
            start_game("Ava")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# GAME SCREEN
# -----------------------------
else:
    left, right = st.columns([2, 1])

    with left:
        st.markdown('<div class="story-panel">', unsafe_allow_html=True)

        scene_text = st.session_state.last_response.strip()
        reflection_text = extract_reflection(scene_text)

        if st.session_state.final_result:
            st.markdown('<div class="scene-badge">FINAL RESULT</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="scene-badge">Scene {st.session_state.current_scene} of 5</div>',
                unsafe_allow_html=True
            )

        safe_story = scene_text if scene_text else "Story response is empty."

        st.markdown(f"""
        <div class="story-text">{safe_story}</div>
        """, unsafe_allow_html=True)

        if reflection_text and not st.session_state.final_result:
            st.markdown(f"""
            <div class="reflection-box">
                <b>Reflection Insight:</b> {reflection_text}
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.progress(min(st.session_state.current_scene, 5) / 5)

        if not st.session_state.final_result:
            choices = parse_choices(scene_text)

            if len(choices) == 3:
                st.markdown("### Choose what happens next:")
                c1, c2, c3 = st.columns(3)

                with c1:
                    if st.button(f"A) {choices[0]}", use_container_width=True):
                        send_choice(f"A) {choices[0]}")
                        st.rerun()

                with c2:
                    if st.button(f"B) {choices[1]}", use_container_width=True):
                        send_choice(f"B) {choices[1]}")
                        st.rerun()

                with c3:
                    if st.button(f"C) {choices[2]}", use_container_width=True):
                        send_choice(f"C) {choices[2]}")
                        st.rerun()
            else:
                st.warning("Choices could not be parsed from the response.")

        with st.expander("Show Raw Flowise Response"):
            st.code(st.session_state.raw_response or "No raw response yet.", language="json")

    with right:
        p = PERSONAS[st.session_state.selected_persona]
        st.markdown('<div class="game-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Current Persona</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="persona-card" style="background:{p['color']}; min-height:180px;">
            <div class="persona-emoji">{p['emoji']}</div>
            <div class="persona-name">{st.session_state.selected_persona}</div>
            <div class="persona-subtitle">{p['subtitle']}</div>
            <div class="persona-desc">{p['description']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="tip-box">', unsafe_allow_html=True)
        st.markdown("**Your Role**")
        st.write("Guide the persona through each scene by choosing the kind of support you want to give.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="tip-box">', unsafe_allow_html=True)
        st.markdown("**Story Progress**")
        if st.session_state.final_result:
            st.write("The story has reached its ending.")
        else:
            st.write(f"You are currently in Scene {st.session_state.current_scene} of 5.")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🔄 Restart Game", use_container_width=True):
            restart_game()
            st.rerun()

# -----------------------------
# FOOTER
# -----------------------------
st.markdown(
    "<div class='footer-note'>Interactive wellness storytelling powered by Aanya 💚</div>",
    unsafe_allow_html=True
)
