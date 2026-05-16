import streamlit as st
import base64
import os

def render_sidebar():
    with st.sidebar:
        # Render Official Brand Logo
        try:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo_cropped.png")
            with open(logo_path, "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
            logo_html = f'<div style="height: 85px; overflow: hidden; display: flex; align-items: center; justify-content: center; margin-top: -10px; margin-bottom: 12px;"><img src="data:image/png;base64,{logo_b64}" style="width: 100%; max-width: 170px;" alt="SynapseAI Logo"></div>'
            st.markdown(logo_html, unsafe_allow_html=True)
        except Exception:
            st.markdown("<h2 style='text-align: center; color: var(--dark-indigo); margin-top: -20px; margin-bottom: 16px;'>SynapseAI</h2>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: var(--text-secondary); letter-spacing: 0.05em; margin-bottom: 8px;'>Main Navigation</p>", unsafe_allow_html=True)
        
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard"
            
        nav_items = [
            ("Dashboard", ":material/dashboard:"),
            ("AI Chat", ":material/forum:"),
            ("Summaries", ":material/description:"),
            ("Quiz Generator", ":material/quiz:"),
            ("Study Planner", ":material/calendar_today:")
        ]
        
        for name, icon_sym in nav_items:
            # Make button feel sleek
            is_active = st.session_state.current_page == name
            btn_type = "primary" if is_active else "secondary"
            
            if st.button(name, use_container_width=True, key=f"nav_{name}", type=btn_type, icon=icon_sym):
                st.session_state.current_page = name
                st.rerun()
                
        st.markdown("<hr style='margin: 20px 0; border-color: rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: var(--text-secondary); letter-spacing: 0.05em; margin-bottom: 8px;'>Settings</p>", unsafe_allow_html=True)
        
        if st.button("Reset Memory", use_container_width=True, icon=":material/delete_sweep:"):
            from utils.memory import clear_memory
            clear_memory()
            st.toast("🚀 Memory & Knowledge base completely purged!", icon="✅")
            import time
            time.sleep(0.8) # Let user see toast
            st.rerun()
            
        st.markdown("""
        <div style="margin-top: 40px; text-align: center; opacity: 0.6; font-size: 0.7rem; color: var(--text-secondary); font-weight: 600; letter-spacing: 0.03em; text-transform: uppercase;">
            SynapseAI Enterprise
        </div>
        """, unsafe_allow_html=True)
