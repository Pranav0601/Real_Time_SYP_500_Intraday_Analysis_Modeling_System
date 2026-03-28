# apps/dashboard/app.py

import streamlit as st
import requests

st.title("S&P 500 Daily Low Predictor")

# call API
response = requests.get("http://127.0.0.1:8000/predict")

if response.status_code == 200:
    data = response.json()

    st.metric("Current Low", data["low_so_far"])
    st.metric("Probability Low Holds", round(data["probability"], 2))

else:
    st.error("Failed to fetch prediction")