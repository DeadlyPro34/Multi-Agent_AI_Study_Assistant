import streamlit as st
import base64
import os

def render_navbar():
    # Initialize notifications array if missing
    if "notifications" not in st.session_state:
        st.session_state.notifications = []

    # Render Official Brand Logo in Header
    try:
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo_cropped.png")
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<div style="display: flex; align-items: center; height: 52px;"><img src="data:image/png;base64,{logo_b64}" style="height: 48px;" alt="SynapseAI Logo"></div>'
    except Exception:
        logo_html = '<div style="display: flex; align-items: center; height: 52px;"><span style="font-weight: 800; font-size: 1.3rem; color: var(--dark-indigo); letter-spacing: -0.02em;">SynapseAI</span></div>'

    # Style Injection to Force the Streamlit Popover Button and Content into a Premium Light Theme
    st.markdown("""
    <style>
    /* 1. THE DEFINITIVE HEADER BUTTON OVERRIDE */
    div[data-testid="stPopover"] button,
    button[kind="secondary"],
    [data-testid="stBaseButton-secondary"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 20px !important;
        color: var(--dark-indigo) !important;
        font-weight: 700 !important;
        padding: 6px 18px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
        height: 38px !important;
    }

    div[data-testid="stPopover"] button:hover {
        border-color: var(--primary-indigo) !important;
        background-color: #F8FAFC !important;
        color: var(--primary-indigo) !important;
    }

    /* 2. THE TOTAL POPOVER LIGHT-OUT: Kill backgrounds on EVERYTHING inside */
    div[data-testid="stPopoverContent"],
    div[data-testid="stPopoverBody"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border-radius: 16px !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.18) !important;
        color: var(--text-main) !important;
    }

    /* Targeted wildcard: Kill background on all nested elements inside the popover */
    div[data-testid="stPopoverContent"] * {
        background-color: transparent !important;
        background: transparent !important;
    }

    /* Force restore card gradients (they need their backgrounds back) */
    div[data-testid="stPopoverContent"] div[style*="background: linear-gradient"] {
        background: inherit !important; /* Allow the specific inline style to persist */
    }

    /* 3. ENFORCE TYPOGRAPHY COLORS */
    div[data-testid="stPopoverContent"] h4,
    div[data-testid="stPopoverContent"] h4 span,
    div[data-testid="stPopoverContent"] .material-icons-round {
        color: var(--dark-indigo) !important;
    }

    div[data-testid="stPopoverContent"] p,
    div[data-testid="stPopoverContent"] div {
        color: var(--text-main) !important;
    }

    /* Custom Scroll Area */
    .notif-scroll-area {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px 20px 20px 20px;
        background: #FFFFFF !important;
        border-radius: 0 0 16px 16px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Master Header Container Flex Layout
    header_col, act_col = st.columns([1, 1])
    
    with header_col:
        st.markdown(logo_html, unsafe_allow_html=True)
        
    with act_col:
        # Use nested columns for exact alignment of the widgets aligned to the far right
        r1, r2 = st.columns([1, 0.6])
        
        with r1:
            notifs = st.session_state.notifications
            notif_count = len(notifs)
            
            # Dynamic label with counting logic
            bell_label = f":material/notifications: {notif_count} notification{'s' if notif_count != 1 else ''}"
            
            # Render the interactive Popover Center
            with st.popover(bell_label, use_container_width=True):
                st.markdown("<h4 style='margin-top:0; margin-bottom:12px; color: var(--dark-indigo); font-size:1.1rem; display:flex; align-items:center; gap:8px;'><span class='material-icons-round'>notifications_active</span> Activity Center</h4>", unsafe_allow_html=True)
                
                if not notifs:
                    st.markdown("<div style='text-align: center; padding: 40px 0; color: var(--text-secondary); font-size:0.9rem;'>🛸 No active alerts.<br>All quiet on the dashboard.</div>", unsafe_allow_html=True)
                else:
                    # USE NATIVE STREAMLIT CONTAINER FOR STABLE SCROLLING
                    with st.container(height=380, border=False):
                        # Loop through in reverse chronological order (newest first)
                        for idx, item in enumerate(reversed(notifs)):
                            is_completed = item["status"] == "COMPLETED"
                            
                            # Premium Minimalist Cards
                            if is_completed:
                                border_clr = "#10B981"
                                icon = "✅"
                            else:
                                border_clr = "#EF4444"
                                icon = "⚠️"
                            
                            st.markdown(f"""
                            <div style='border-left: 3px solid {border_clr}; padding-left: 12px; margin-bottom: 16px;'>
                                <div style='font-size: 0.9rem; font-weight: 600; color: var(--text-main); line-height: 1.3;'>{icon} {item['message']}</div>
                                <div style='font-size: 0.75rem; color: var(--text-secondary); margin-top: 4px;'>{item['timestamp']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Clickable Action Button
                            if is_completed:
                                btn_lbl = "📖 Load Summary"
                                if item["type"] == "quiz":
                                    btn_lbl = "📝 Start Quiz"
                                elif item["type"] == "planner":
                                    btn_lbl = "📅 View Roadmap"
                                elif item["type"] == "chat":
                                    btn_lbl = "💬 View Reply"
                                    
                                if st.button(btn_lbl, key=f"notif_btn_{item['id']}_{idx}", type="secondary", use_container_width=True):
                                    if item["type"] == "summary":
                                        st.session_state.current_page = "Summaries"
                                        st.session_state.summary_content = item["result"]
                                        st.session_state.summary_active = True
                                    elif item["type"] == "planner":
                                        st.session_state.current_page = "Study Planner"
                                        st.session_state.plan_content = item["result"]
                                        st.session_state.plan_active = True
                                    elif item["type"] == "chat":
                                        st.session_state.current_page = "AI Chat"
                                    elif item["type"] == "quiz":
                                        from components.quiz_ui import extract_json_quiz
                                        quiz_data = extract_json_quiz(item["result"])
                                        if quiz_data and "questions" in quiz_data:
                                            st.session_state.current_page = "Quiz Generator"
                                            st.session_state.quiz_questions = quiz_data["questions"]
                                            st.session_state.quiz_active = True
                                    st.rerun()
                    
                    # Bottom Actions
                    st.divider()
                    if st.button("🧹 Clear Activity Log", use_container_width=True, icon=":material/delete_sweep:"):
                        st.session_state.notifications = []
                        st.rerun()
        
        with r2:
            # Explicitly align User Profile Badge
            st.markdown(f"""
            <div style="font-size: 0.85rem; background: linear-gradient(135deg, var(--primary-indigo), var(--primary-lavender)); height: 38px; padding: 0 14px; border-radius: 20px; color: #fff; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 4px; cursor: default;">
                <span class="material-icons-round" style="font-size: 1.1rem;">account_circle</span> User
            </div>
            """, unsafe_allow_html=True)

    # Elegant thin border under the master header
    st.markdown("<div style='margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color);'></div>", unsafe_allow_html=True)

