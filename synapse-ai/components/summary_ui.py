import streamlit as st
from utils.rag_pipeline import VectorStore
from agents.crew_setup import run_study_crew
from utils.async_manager import start_background_task, check_task_status

@st.fragment(run_every=1.5)
def auto_poll_summary():
    if st.session_state.get("summary_task_id"):
        task = check_task_status(st.session_state.summary_task_id)
        if task:
            if task["status"] == "COMPLETED":
                st.session_state.summary_content = task["result"]
                st.session_state.summary_active = True
                st.session_state.summary_task_id = None
                st.rerun()
            elif task["status"] == "FAILED":
                st.error(f"🚨 Summarization Failed: {task['result']}")
                st.session_state.summary_task_id = None
                st.rerun()

def render_summary_ui():
    # Initialize state
    if "summary_active" not in st.session_state:
        st.session_state.summary_active = False
    if "summary_content" not in st.session_state:
        st.session_state.summary_content = ""
    if "summary_task_id" not in st.session_state:
        st.session_state.summary_task_id = None

    if st.session_state.summary_task_id:
        auto_poll_summary()

    st.markdown("""
    <style>
    .summary-card {
        background: var(--bg-card);
        padding: 32px;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.02);
    }
    .badge {
        background: rgba(79, 70, 229, 0.1);
        color: var(--primary-indigo);
        padding: 6px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(79, 70, 229, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # --- 1. ACTIVE BACKGROUND INGESTION VIEW ---
    if st.session_state.summary_task_id:
        st.markdown("""
<div class='glass-card' style='padding: 40px; text-align: center; margin-bottom: 2rem;'>
<div style='font-size: 3.5rem; margin-bottom: 1.5rem;'>🧠🛸⚡</div>
<h2 style='margin-top:0; color: var(--dark-indigo);'>Generating Distilled Study Notes...</h2>
<p style='color: var(--text-secondary); font-size: 0.95rem; max-width: 600px; margin: 0 auto 1.5rem auto;'>
    Our AI Summarizer Agent is hard at work mapping concepts and synthesizing facts in the background!
</p>
<div style='background: rgba(79, 70, 229, 0.05); border: 1px dashed var(--primary-indigo); border-radius: 12px; padding: 16px; font-size: 0.9rem; color: var(--primary-indigo); font-weight: 500;'>
    🚀 Feel free to switch tabs, ask questions in <b>AI Chat</b>, or build a plan! 
    We will automatically alert the <b>Notification Bell</b> in the header the moment it finishes!
</div>
</div>
""", unsafe_allow_html=True)
        
        with st.spinner("Agent processing document sectors..."):
            st.button("🔄 Check Work Progress Now", use_container_width=True)

    # --- 2. CONFIGURATION SCREEN ---
    elif not st.session_state.summary_active:
        st.markdown("""
<div class='glass-card' style='padding: 32px; text-align: center; margin-bottom: 2rem;'>
<span class="material-icons-round" style='font-size: 3.5rem; background: linear-gradient(135deg, #4F46E5, #7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; display: inline-block;'>auto_stories</span>
<h2 style='margin-top:0; color: var(--dark-indigo);'>Knowledge Engine: Intelligent Summaries</h2>
<p style='color: var(--text-secondary); font-size: 0.95rem; max-width: 600px; margin: 0 auto;'>
Instantly distill massive documents into actionable revision notes. Select your subject depth 
and format below to have our summarizer agent extract the exact essentials.
</p>
</div>
""", unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            summary_topic = st.text_input(":material/topic: Chapter, Unit, or Concept:", placeholder="e.g., 'JVM Internals', 'UNIT 3 3D Viewing' (leave blank for full book summary)")
            summary_depth = st.selectbox(":material/auto_stories: Summary Depth & Detail:", 
                                       options=["Fast-Recall Cheat Sheet (High Level)", "Structured Exam Study Guide (Medium)", "Deep Concept Breakdown (Comprehensive)"])
        with col2:
            summary_style = st.radio(":material/rule: Organization Layout:", 
                                    options=["Hierarchical Lists & Bullets", "Narrative Explanation Blocks", "Key Facts & Code Only"])

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

        if st.button("📚 Generate Study Summary", type="primary", use_container_width=True, icon=":material/auto_stories:", disabled=bool(st.session_state.summary_task_id)):
            # Fetch deep context synchronously (fast step)
            with st.spinner("Analyzing knowledge base context..."):
                vector_store = VectorStore()
                query = summary_topic if summary_topic.strip() else "Course Chapter Syllabus Core Outline"
                context_chunks = vector_store.search(query, top_k=5)
                context_str = "\n---\n".join(context_chunks) if context_chunks else ""
                context_str = context_str[:3500]

            task_desc = (
                f"Generate a comprehensive {summary_depth} summary for the topic: '{summary_topic if summary_topic.strip() else 'Full Document Material'}'. "
                f"Enforce this visual layout format: '{summary_style}'. "
                f"Synthesize and extract the single most critical elements, definitions, formulas, or code patterns."
            )

            topic_title = summary_topic.strip() if summary_topic.strip() else "All Knowledge Base"

            # SPAWN BACKGROUND THREAD instead of blocking!
            # Arguments passed to run_study_crew positionally: (task_description, task_type, context)
            task_id = start_background_task("summary", topic_title, run_study_crew, task_desc, "summary", context_str)
            st.session_state.summary_task_id = task_id
            st.rerun()

    # --- ACTIVE DISPLAY SCREEN ---
    else:
        st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;'>
            <h2 style='margin: 0; color: var(--dark-indigo); display:flex; align-items:center; gap:8px;'>
                <span class="material-icons-round" style="color: var(--primary-indigo);">menu_book</span> Distilled Knowledge Card
            </h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='summary-card'>", unsafe_allow_html=True)
        st.markdown(st.session_state.summary_content)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🔄 Summarize Another Topic", type="primary", use_container_width=True, icon=":material/refresh:"):
            st.session_state.summary_active = False
            st.session_state.summary_content = ""
            st.rerun()
