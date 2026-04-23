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
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1rem;
        max-width: 1300px;
    }

    .hero-box {
        background: linear-gradient(135deg, #dbeafe, #eef2ff);
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        margin-bottom: 1rem;
        border: 1px solid #dbe4ff;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #4b5563;
    }

    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
        text-align: center;
        min-height: 95px;
    }

    .section-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1f2937;
        margin-top: 0.3rem;
        margin-bottom: 0.5rem;
    }

    .scene-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    .scene-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }

    .reflection-box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem;
        margin-top: 1rem;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
    }

    .footer-note {
        text-align: center;
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: 1rem;
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
            "content": "Hi, I’m your anxiety support persona. I’m here to listen and guide you gently. How are you feeling today?"
        }
    ]

if "selected_persona" not in st.session_state:
    st.session_state.selected_persona = "Anxiety Support"

if "mood" not in st.session_state:
    st.session_state.mood = "Stressed"

if "reflection_notes" not in st.session_state:
    st.session_state.reflection_notes = ""

# -----------------------------
# Scene descriptions
# -----------------------------
scene_descriptions = {
    "Calm": {
        "emoji": "🌅",
        "title": "Calm Reflection Space",
        "desc": "A soft sunrise, warm light, and a quiet space that supports grounding and gentle reflection."
    },
    "Okay": {
        "emoji": "🌿",
        "title": "Balanced Wellness Space",
        "desc": "A peaceful room with plants and natural light, representing emotional balance and steady energy."
    },
    "Stressed": {
        "emoji": "☁️",
        "title": "Busy Mind Scene",
        "desc": "A cloudy atmosphere and a full workspace reflecting pressure, deadlines, and emotional overload."
    },
    "Anxious": {
        "emoji": "🌧️",
        "title": "Anxiety Support Scene",
        "desc": "A rainy window, dim lighting, and a quiet room reflecting overthinking, tension, and emotional heaviness."
    },
    "Overwhelmed": {
        "emoji": "🌊",
        "title": "Overwhelm Recovery Scene",
        "desc": "A heavy emotional scene showing mental overload, with space for slowing down and regaining control."
    }
}

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
        index=0
    )

    st.markdown("### Check-in")
    st.session_state.mood = st.radio(
        "How are you feeling today?",
        ["Calm", "Okay", "Stressed", "Anxious", "Overwhelmed"],
        index=2
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
            "content": "Let’s pause. Inhale for 4... hold for 4... exhale for 6. Repeat that three times slowly."
        })
        st.rerun()

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">The Resilience Game</div>
    <div class="hero-subtitle">
        An interactive AI wellness experience for reflection, emotional awareness, and personal growth.
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
# Scene visual generator
# -----------------------------
def generate_scene_html(mood):
    color_map = {
        "Calm": ("#d1fae5", "#ecfdf5", "linear-gradient(135deg, #d1fae5, #ecfdf5)"),
        "Okay": ("#dcfce7", "#f0fdf4", "linear-gradient(135deg, #dcfce7, #f0fdf4)"),
        "Stressed": ("#e0f2fe", "#f8fafc", "linear-gradient(135deg, #e0f2fe, #f8fafc)"),
        "Anxious": ("#dbeafe", "#eff6ff", "linear-gradient(135deg, #dbeafe, #eff6ff)"),
        "Overwhelmed": ("#ede9fe", "#f5f3ff", "linear-gradient(135deg, #ede9fe, #f5f3ff)")
    }

    emoji = scene_descriptions[mood]["emoji"]
    title = scene_descriptions[mood]["title"]
    desc = scene_descriptions[mood]["desc"]
    _, _, gradient = color_map[mood]

    return f"""
    <div style="
        background: {gradient};
        border-radius: 18px;
        padding: 2rem 1rem;
        text-align: center;
        border: 1px solid #dbe4ff;
        min-height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 1px 6px rgba(0,0,0,0.04);
    ">
        <div style="font-size: 4.5rem; margin-bottom: 0.5rem;">{emoji}</div>
        <div style="font-size: 1.2rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem;">{title}</div>
        <div style="font-size: 0.95rem; color: #4b5563; max-width: 85%;">
            {desc}
        </div>
    </div>
    """

# -----------------------------
# Main layout: Scene + Chat
# -----------------------------
left_col, right_col = st.columns([1, 2])

with left_col:
    st.markdown('<div class="scene-card"><div class="scene-title">Current Scene Visual</div></div>', unsafe_allow_html=True)
    st.markdown(generate_scene_html(st.session_state.mood), unsafe_allow_html=True)

    st.markdown('<div class="reflection-box">', unsafe_allow_html=True)
    st.markdown("### Reflection Note")
    st.session_state.reflection_notes = st.text_area(
        "Write a short reflection",
        value=st.session_state.reflection_notes,
        height=140,
        label_visibility="collapsed",
        placeholder="Write what you are feeling, what triggered it, or what helped today..."
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown("### Conversation")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# -----------------------------
# Replace this with Flowise API call
# -----------------------------
def get_bot_response(user_text: str, mood: str, persona: str) -> str:
    return (
        f"You’re speaking with the {persona} persona, and I can sense you may be feeling {mood.lower()}. "
        f"You said: '{user_text}'. That sounds important. Can you tell me a little more about what triggered this feeling?"
    )

# -----------------------------
# Chat input
# -----------------------------
user_input = st.chat_input("Share what’s on your mind...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    bot_reply = get_bot_response(
        user_input,
        st.session_state.mood,
        st.session_state.selected_persona
    )

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    "<div class='footer-note'>Built with Streamlit for a more interactive and empathetic wellness experience.</div>",
    unsafe_allow_html=True
)
