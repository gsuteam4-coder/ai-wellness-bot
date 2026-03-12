import streamlit as st

st.title("Mental Wellness Simulation")

# Patient scenario
with st.chat_message("assistant"):
    st.write("Hi... I'm Alex. Lately my days feel overwhelming and I’m not sure why.")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
    
if "answers" not in st.session_state:
    st.session_state.answers = []    

# QUESTION 1
if st.session_state.step == 1:

    st.write("Aanya: When Alex wakes up in the morning, what feeling appears first?")

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

# QUESTION 2
elif st.session_state.step == 2:

    st.write("Aanya: How does Alex usually feel during the day?")

    col1, col2, col3 = st.columns(3)

    if col1.button("A) Constant pressure"):
        st.session_state.step = 3

    if col2.button("B) Low energy"):
        st.session_state.step = 3

    if col3.button("C) Mentally exhausted"):
        st.session_state.step = 3

# QUESTION 3
elif st.session_state.step == 3:

    st.write("Aanya: What happens in the evening?")

    col1, col2, col3 = st.columns(3)

    if col1.button("A) Overthinking about tasks"):
        st.session_state.step = 4

    if col2.button("B) Feeling drained"):
        st.session_state.step = 4

    if col3.button("C) Just wanting to escape everything"):
        st.session_state.step = 4

# FINAL MESSAGE
elif st.session_state.step == 4:

    answers = st.session_state.answers

    if "pressure" in answers:
        message = "It sounds like Alex is carrying a lot of pressure throughout the day."

    elif "tired" in answers:
        message = "It seems like Alex may be struggling with low energy and rest."

    else:
        message = "It seems Alex may be feeling emotionally drained."

    st.write("Aanya:")
    st.write(message)
    st.write("Sometimes starting with one small step during the day can help create a sense of balance.")


st.write("---")

if st.button("Restart Simulation"):
    st.session_state.step = 1
    st.session_state.answers = []
