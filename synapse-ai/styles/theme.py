import streamlit as st
import os

def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "main.css")
    try:
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Running without custom styles.")
