import streamlit as st
import requests

st.title("AI Mental Wellness Diagnostic Bot")

st.write("Talk with the AI diagnostic bot about your mental wellness.")

user_input = st.text_input("How are you feeling today?")

if user_input:

    url = "https://cloud.flowiseai.com/api/v1/prediction/7b60721f-874f-4f0a-a811-ca1f43c0d1fd"

    payload = {
        "question": user_input
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        result = response.json()
        st.write(result["text"])
    else:
        st.write("Error connecting to AI bot.")
