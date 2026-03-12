import streamlit as st

st.title("Mental Wellness Simulation")

# Patient scenario
st.write("Patient: Alex")
st.write("Alex is a college student who works part-time and has been feeling overwhelmed recently.")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1

# QUESTION 1
if st.session_state.step == 1:

    st.write("Aanya: When Alex wakes up in the morning, what feeling appears first?")

    col1, col2, col3 = st.columns(3)

    if col1.button("A) Pressure about everything to finish"):
        st.session_state.step = 2

    if col2.button("B) Just tired like sleep wasn’t enough"):
        st.session_state.step = 2

    if col3.button("C) Heavy feeling, hard to start the day"):
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

    st.write("Aanya:")
    st.write(
        "It seems like Alex has been carrying a lot of pressure throughout the day. "
        "Starting the morning already feeling overwhelmed can slowly drain energy and motivation. "
        "Sometimes beginning the day with just one small task can help create a sense of control and momentum."
    )
