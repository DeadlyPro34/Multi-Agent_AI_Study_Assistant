import streamlit as st

def feature_card(title, description, icon):
    st.markdown(f"""
    <div class="glass-card">
        <div style="background: #EEF2FF; color: var(--primary-indigo); width: 48px; height: 48px; border-radius: 10px; display: flex; align-items: center; justify-content: center; border: 1px solid #E0E7FF;">
            <span class="material-icons-round" style="font-size: 1.5rem;">{icon}</span>
        </div>
        <h3>{title}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)
