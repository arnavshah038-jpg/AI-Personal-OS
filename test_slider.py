import streamlit as st

st.set_page_config(
    page_title="Slider Test",
)

st.title("Slider Test")

value = st.slider(
    "Importance",
    min_value=1,
    max_value=10,
    value=5,
)

st.write("Current Value:", value)
