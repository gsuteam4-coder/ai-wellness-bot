import os
import streamlit as st
from datetime import datetime

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="The Resilience Game",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 1300px;
    }

    .hero-box {
        background: linear-gradient(135deg, #14b8a6, #2563eb);
        padding: 1.5rem 1.7rem;
        border-radius: 22px;
        margin-bottom: 1rem;
        box-shadow: 0 10px 28px rgba(0,0,0,0.22);
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.25rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #ecfeff;
    }

    .metric-card {
        background: rgba(255,255,255,0.08);
        padding: 1rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 1px 10px rgba(0,0,0,0.10);
        text-align: center;
        color: white;
        min-height: 95px;
    }

    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: white;
        margin-top: 0.2rem;
        margin-bottom: 0.6rem;
    }

    .panel-box {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    }

    .scene-info-box {
        background: rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1rem;
        color: #e5e7eb;
        margin-top: 0.8rem;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .scene-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.3rem;
    }

    .scene-desc {
        font-size: 0.96rem;
        line-height: 1.6;
        color: #dbeafe;
    }

    .fallback-scene {
        min-height: 320px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        text-align: center;
        padding: 2rem;
        color: white;
        background: linear-gradient(135deg, #1e3a8a, #0f766e, #7c3aed);
        border: 1px solid rgba(255,255,255,0.10);
    }

    .fallback-emoji {
        font-size: 4rem;
        margin-bottom: 0.6rem;
    }

    .fallback-title {
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
    }

    .fallback-text {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #e0f2fe;
        max-width: 90%;
    }

    .stChatMessage {
        border-radius: 16px;
        padding: 0.25rem;
    }

    .stChatMessage [data-testid="stMarkdownContainer"] p {
        font-size: 1rem;
        line-height: 1.6;
    }

    .footer-note {
        text-align: center;
        color: #cbd5e1;
        font-size: 0.88rem;
        margin-top: 1.2rem;
    }

    div[data-testid="stButton"] > button {
        border-radius: 14px !important;
        min-height: 48px;
        font-weight: 700;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi, I’m your support persona. I’m here to guide you gently through this wellness experience. How are you feeling today?"
        }
    ]

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = "Anxiety Support"

if "mood" not in st.session_state:
    st.session_state.mood = "Stressed"

# -----------------------------
# Image mappings
# -----------------------------
persona_images = {
    "Anxiety Support": "images/anxiety_support.jpg",
    "Burnout Support": "images/burnout_support.jpg",
    "Stress Reflection": "images/stress_reflection.jpg"
}

mood_images = {
    "Calm": "images/calm.jpg",
    "Okay": "images/okay.jpg",
    "Stressed": "images/stressed.jpg",
    "Anxious": "images/anxious.jpg",
    "Overwhelmed": "images/overwhelmed.jpg"
}

scene_descriptions = {
    "Calm": {
        "emoji": "🌅",
        "title": "Calm Reflection Scene",
        "desc": "A quiet and peaceful setting that supports self-awareness, grounding, and emotional balance."
    },
    "Okay": {
        "emoji": "🌿",
        "title": "Steady Wellness Scene",
        "desc": "A balanced space showing emotional stability, light energy, and room for gentle reflection."
    },
    "Stressed": {
        "emoji": "☁️",
        "title": "Pressure and Deadlines Scene",
        "desc": "A tense environment reflecting workload, mental clutter, and the need to pause before overwhelm builds further."
    },
    "Anxious": {
        "emoji": "🌧️",
        "title": "Anxiety Support Scene",
        "desc": "A heavier emotional space reflecting overthinking, social tension, worry, and the need for support."
    },
    "Overwhelmed": {
        "emoji": "🌊",
        "title": "Overwhelm Recovery Scene",
        "desc": "A mentally overloaded scene where rest, clarity, and emotional regulation become most important."
    }
}

# -----------------------------
# Helpers
# -----------------------------
def get_scene_image():
    persona_img = persona_images.get(st.session_state.selected_persona)
    mood_img = mood_images.get(st.session_state.mood)

    if mood_img and os.path.exists(mood_img):
        return mood_img
    if persona_img and os.path.exists(persona_img):
        return persona_img
    return None

def render_fallback_scene():
    scene = scene_descriptions.get(st.session_state.mood, scene_descriptions["Stressed"])
    st.markdown(f"""
    <div class="fallback-scene">
        <div class="fallback-emoji">{scene['emoji']}</div>
        <div class="fallback-title">{scene['title']}</div>
        <div class="fallback-text">{scene['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("🌿 Resilience Game")
    st.caption("Human-Centered AI for Wellness")

    st.markdown("### Persona")
    st.session_state.selected_persona = st.selectbox(
        "Choose persona",
        ["Anxiety Support", "Burnout Support", "Stress Reflection"],
        index=["Anxiety Support", "Burnout Support", "Stress Reflection"].index(st.session_state.selected_persona)
    )

    st.markdown("### Check-in")
    st.session_state.mood = st.radio(
        "How are you feeling today?",
        ["Calm", "Okay", "Stressed", "Anxious", "Overwhelmed"],
        index=["Calm", "Okay", "Stressed", "Anxious", "Overwhelmed"].index(st.session_state.mood)
    )

    st.markdown("### Session Tools")
    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Chat cleared. I’m here with you. What would you like to talk about now?"
            }
        ]
        st.rerun()

    if st.button("📝 Reflection Prompt", use_container_width=True):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Take a moment to reflect: What has been the heaviest thing on your mind this week?"
        })
        st.rerun()

    if st.button("💙 Breathing Exercise", use_container_width=True):
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Let’s pause for a short breathing exercise. Inhale for 4... hold for 4... exhale for 6. Repeat three times."
        })
        st.rerun()

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">💚 The Resilience Game</div>
    <div class="hero-subtitle">
        An interactive wellness experience using AI personas, scene visuals, reflection, and emotional support.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Top metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="section-title">Active Persona</div>
        <div>{st.session_state.selected_persona}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="section-title">Current Mood</div>
        <div>{st.session_state.mood}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    current_time = datetime.now().strftime("%I:%M %p")
    st.markdown(f"""
    <div class="metric-card">
        <div class="section-title">Session Time</div>
        <div>{current_time}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Quick start buttons
# -----------------------------
st.markdown("### Quick Start")

q1, q2, q3, q4 = st.columns(4)
with q1:
    if st.button("I feel anxious", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "I feel anxious today."})
        st.rerun()

with q2:
    if st.button("I’m overthinking", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "I’m overthinking everything."})
        st.rerun()

with q3:
    if st.button("I need motivation", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "I need motivation and emotional support."})
        st.rerun()

with q4:
    if st.button("Help me calm down", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Can you help me calm down?"})
        st.rerun()

# -----------------------------
# Main layout: Scene + Chat
# -----------------------------
left_col, right_col = st.columns([1.1, 1.4])

with left_col:
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Current Scene</div>', unsafe_allow_html=True)

    scene_image = get_scene_image()
    if scene_image:
        st.image(scene_image, use_container_width=True)
    else:
        render_fallback_scene()

    current_scene = scene_descriptions.get(st.session_state.mood, scene_descriptions["Stressed"])
    st.markdown(f"""
    <div class="scene-info-box">
        <div class="scene-title">{current_scene['title']}</div>
        <div class="scene-desc">{current_scene['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown("### Conversation")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Replace this function with your Flowise/API call
# -----------------------------
def get_bot_response(user_text: str) -> str:
    persona = st.session_state.selected_persona
    mood = st.session_state.mood
    return (
        f"You’re interacting with the {persona} persona. "
        f"I can sense that the current emotional tone is {mood.lower()}. "
        f"You said: '{user_text}'. That sounds important. Can you tell me a little more about what triggered this feeling?"
    )

# -----------------------------
# Chat input
# -----------------------------
user_input = st.chat_input("Share what’s on your mind...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_reply = get_bot_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    "<div class='footer-note'>Built with Streamlit for a more visual and reflective wellness experience.</div>",
    unsafe_allow_html=True
)
