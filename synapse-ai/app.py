import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App configuration
st.set_page_config(
    page_title="SynapseAI | Enterprise Study Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom Theme
from styles.theme import load_css
load_css()

# GLOBAL THEME DEFINITIVE OVERRIDES (Targets stubborn internal blocks)
st.markdown("""
<style>
    /* 1. DEFINE THE LIGHT MODE NUCLEAR OPTION FOR ALL POPOVERS */
    div[data-testid="stPopoverContent"],
    div[data-testid="stPopoverBody"],
    div[data-testid="stPopoverContent"] > div,
    div[data-testid="stPopoverContent"] [data-testid="stVerticalBlock"],
    div[data-testid="stPopoverContent"] [data-testid="stMarkdownContainer"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #1F2937 !important;
    }

    /* Force text visibility against white background */
    div[data-testid="stPopoverContent"] h1, 
    div[data-testid="stPopoverContent"] h2, 
    div[data-testid="stPopoverContent"] h3, 
    div[data-testid="stPopoverContent"] h4, 
    div[data-testid="stPopoverContent"] p, 
    div[data-testid="stPopoverContent"] span {
        color: #1E1B4B !important; /* Dark Indigo */
    }

    /* Target buttons in the header to be white-pill */
    div[data-testid="stPopover"] > button {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 20px !important;
        color: #312E81 !important;
    }
</style>
""", unsafe_allow_html=True)

# Import components
from components.sidebar import render_sidebar
from components.navbar import render_navbar
from components.upload_section import render_upload_section
from components.chat_ui import render_chat_ui
from components.quiz_ui import render_quiz_ui
from components.summary_ui import render_summary_ui
from components.planner_ui import render_planner_ui
from components.cards import feature_card

def main():
    # 0. Sync Background Tasks and Update Global State
    from utils.async_manager import drain_completed_tasks
    if "notifications" not in st.session_state:
        st.session_state.notifications = []
        
    # Poll background workers and append newly finished payloads to stack
    new_notifications = drain_completed_tasks()
    if new_notifications:
        st.session_state.notifications.extend(new_notifications)

    # 1. Render Navigation Shell
    render_sidebar()
    render_navbar()
    
    # API Key Checker
    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "your_gemini_api_key_here":
        st.warning("⚠️ Action Required: Please set your GEMINI_API_KEY in your environment variables.")
    
    current_page = st.session_state.get("current_page", "Dashboard")
    
    if current_page == "Dashboard":
        # Main Dashboard Header
        st.markdown("""
        <div style='margin-bottom: 2rem;'>
            <h1 class='dashboard-title'>Workspace Dashboard</h1>
            <p class='dashboard-subtitle'>Welcome to SynapseAI. Choose an agent or upload a knowledge base to get started.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # High-Level Feature Overview
        col1, col2, col3 = st.columns(3)
        with col1:
            feature_card("Semantic Search & RAG", "Upload your PDFs and retrieve instantaneous contextual data.", "folder")
        with col2:
            feature_card("Specialized AI Modes", "Focused AI study modes specialize in parsing dynamic syllabi.", "psychology")
        with col3:
            feature_card("Optimized Analytics", "Intelligent revision timetables generated autonomously.", "auto_graph")
            
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        
        # Lower Section: Tools & Tips
        left_pane, right_pane = st.columns([2.2, 1])
        
        with left_pane:
            render_upload_section()
            
        with right_pane:
            st.markdown("""
            <div class='glass-card' style='padding: 24px;'>
                <h4 style='margin-top:0; margin-bottom: 12px; font-size: 1rem; color: var(--dark-indigo); display: flex; align-items: center; gap: 8px;'>
                    <span class="material-icons-round" style="color: var(--primary-indigo); font-size: 1.25rem;">rocket_launch</span>
                    Getting Started
                </h4>
                <ol style='padding-left: 1.2rem; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.8;'>
                    <li>Drop your PDFs or text sources into the upload portal.</li>
                    <li>Select <strong>Process Documents</strong> to run vector ingestion.</li>
                    <li>Head over to the <strong>AI Chat</strong> or <strong>Summaries</strong> tab to invoke the specialized agentic workflows.</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            
    elif current_page == "AI Chat":
        st.markdown("""
        <div style='margin-bottom: 1.5rem;'>
            <h1 class='dashboard-title'>Expert Explainer</h1>
            <p class='dashboard-subtitle'>Ask granular questions from your codebase or textbooks.</p>
        </div>
        """, unsafe_allow_html=True)
        render_chat_ui(agent_mode="explain")
        
    elif current_page == "Summaries":
        st.markdown("""
        <div style='margin-bottom: 1.5rem;'>
            <h1 class='dashboard-title'>Intelligent Summarizer</h1>
            <p class='dashboard-subtitle'>Rapidly convert high-volume PDF reading materials into core revision highlights.</p>
        </div>
        """, unsafe_allow_html=True)
        render_summary_ui()
        
    elif current_page == "Quiz Generator":
        st.markdown("""
        <div style='margin-bottom: 1.5rem;'>
            <h1 class='dashboard-title'>Automated Quiz Engine</h1>
            <p class='dashboard-subtitle'>Dynamically test and evaluate your subject matter expertise.</p>
        </div>
        """, unsafe_allow_html=True)
        render_quiz_ui()
        
    elif current_page == "Study Planner":
        st.markdown("""
        <div style='margin-bottom: 1.5rem;'>
            <h1 class='dashboard-title'>AI Study Planner</h1>
            <p class='dashboard-subtitle'>Instantly formulate structured timelines based on custom milestones.</p>
        </div>
        """, unsafe_allow_html=True)
        render_planner_ui()

if __name__ == "__main__":
    main()
