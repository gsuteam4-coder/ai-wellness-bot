import streamlit as st

st.set_page_config(page_title="AI Persona Simulation")

st.title("AI Persona Simulation")
st.caption("Patient Bot interacting with Aanya — Diagnostic Companion")

# Patient introduction
with st.chat_message("user"):
    st.write("Hi... I'm Alex. Lately my days feel overwhelming and I’m not sure why.")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1

if "answers" not in st.session_state:
    st.session_state.answers = []

# -------------------------
# QUESTION 1
# -------------------------
if st.session_state.step == 1:

    with st.chat_message("assistant"):
        st.write("When Alex wakes up in the morning, what feeling appears first?")

    col1, col2, col3 = st.columns(3)

    if col1.button("A) Pressure about everything to finish"):
        st.session_state.answers.append("pressure")
        st.session_state.step = 2

    if col2.button("B) Just tired like sleep wasn’t enough"):
        st.session_state.answers.append("tired")
        st.session_state.step = 2

    if col3.button("C) Heavy feeling, hard to start the day"):
        st.session_state.answers.append("heavy")
        st.session_state.step = 2


# -------------------------
# QUESTION 2
# -------------------------
elif st.session_state.step == 2:

    with st.chat_message("assistant"):
        st.write("How does Alex usually feel during the day?")

    col1, col2, col3 = st.columns(3)

    if col1.button("A) Constant pressure"):
        st.session_state.answers.append("pressure_day")
        st.session_state.step = 3

    if col2.button("B) Low energy"):
        st.session_state.answers.append("low_energy")
        st.session_state.step = 3

    if col3.button("C) Mentally exhausted"):
        st.session_state.answers.append("mental_exhaustion")
        st.session_state.step = 3


# -------------------------
# QUESTION 3
# -------------------------
elif st.session_state.step == 3:

    with st.chat_message("assistant"):
        st.write("What usually happens in the evening?")

    col1, col2, col3 = st.columns(3)

    if col1.button("A) Overthinking about tasks"):
        st.session_state.answers.append("overthinking")
        st.session_state.step = 4

    if col2.button("B) Feeling drained"):
        st.session_state.answers.append("drained")
        st.session_state.step = 4

    if col3.button("C) Wanting to escape everything"):
        st.session_state.answers.append("escape")
        st.session_state.step = 4


# -------------------------
# FINAL ANALYSIS
# -------------------------
elif st.session_state.step == 4:

    answers = st.session_state.answers

    if "pressure" in answers or "pressure_day" in answers:
        message = (
            "It seems Alex may be carrying a lot of pressure throughout the day. "
            "Starting the morning already thinking about unfinished tasks can slowly drain energy and motivation."
        )

    elif "tired" in answers or "low_energy" in answers:
        message = (
            "It looks like Alex may be struggling with low energy and not feeling properly rested. "
            "When sleep and recovery are not enough, the whole day can feel heavier than it should."
        )

    else:
        message = (
            "Alex may be feeling emotionally drained and mentally overwhelmed. "
            "When thoughts keep circling and there’s no space to slow down, it can make everything feel exhausting."
        )

    with st.chat_message("assistant"):
        st.write(message)
        st.write(
            "Sometimes beginning the day with one small manageable task can help create a sense of control and momentum."
        )


# -------------------------
# RESTART BUTTON
# -------------------------
st.write("---")

if st.button("Restart Simulation"):
    st.session_state.step = 1
    st.session_state.answers = []
    st.rerun()
