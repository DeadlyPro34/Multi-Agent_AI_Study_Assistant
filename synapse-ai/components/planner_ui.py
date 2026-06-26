import streamlit as st
from utils.rag_pipeline import VectorStore
from agents.crew_setup import run_study_crew

from utils.async_manager import start_background_task, check_task_status

@st.fragment(run_every=1.5)
def auto_poll_planner():
    if st.session_state.get("planner_task_id"):
        task = check_task_status(st.session_state.planner_task_id)
        if task:
            if task["status"] == "COMPLETED":
                st.session_state.plan_content = task["result"]
                st.session_state.plan_active = True
                st.session_state.planner_task_id = None
                st.rerun()
            elif task["status"] == "FAILED":
                st.error(f"🚨 Planner Agent Generation Failed: {task['result']}")
                st.session_state.planner_task_id = None
                st.rerun()

def render_planner_ui():
    # Initialize session state
    if "plan_active" not in st.session_state:
        st.session_state.plan_active = False
    if "plan_content" not in st.session_state:
        st.session_state.plan_content = ""
    if "planner_task_id" not in st.session_state:
        st.session_state.planner_task_id = None

    if st.session_state.planner_task_id:
        auto_poll_planner()
        
    st.markdown("""
    <style>
    .blueprint-container {
        background: var(--bg-card);
        padding: 30px;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.02);
    }
    .blueprint-header {
        background: linear-gradient(135deg, #4F46E5, #7C3AED);
        color: white !important;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .plan-meta {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 0.9rem;
        display: inline-block;
        margin-right: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    # --- 0. ACTIVE BACKGROUND LOADING ---
    if st.session_state.planner_task_id:
        st.markdown("""
<div class='glass-card' style='padding: 40px; text-align: center; margin-bottom: 2rem;'>
<div style='font-size: 3.5rem; margin-bottom: 1.5rem;'>📅🧩⚡</div>
<h2 style='margin-top:0; color: var(--dark-indigo);'>Building Your Optimization Roadmap...</h2>
<p style='color: var(--text-secondary); font-size: 0.95rem; max-width: 600px; margin: 0 auto 1.5rem auto;'>
    The AI Study Planner is actively structuring schedules and computing intensity loads.
</p>
<div style='background: rgba(79, 70, 229, 0.05); border: 1px dashed var(--primary-indigo); border-radius: 12px; padding: 16px; font-size: 0.9rem; color: var(--primary-indigo); font-weight: 500;'>
    ⚡ Go ahead and explore the <b>AI Chat</b> or test your skills in <b>Quiz Mode</b>!
    As soon as the academic plan is complete, we will sound the <b>Notification Bell</b>.
</div>
</div>
""", unsafe_allow_html=True)
        with st.spinner("Orchestrating study slot breakdowns..."):
            st.button("🔄 Refresh Blueprint Status", use_container_width=True)

    # --- CONFIGURATION PHASE ---
    elif not st.session_state.plan_active:
        st.markdown("""
<div class='glass-card' style='padding: 32px; text-align: center; margin-bottom: 2rem;'>
<span class="material-icons-round" style='font-size: 3.5rem; background: linear-gradient(135deg, #4F46E5, #7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; display: inline-block;'>calendar_today</span>
<h2 style='margin-top:0; color: var(--dark-indigo);'>Build Your Success Blueprint</h2>
<p style='color: var(--text-secondary); font-size: 0.95rem; max-width: 600px; margin: 0 auto;'>
Define your subject matter, timeframe, and preferred study intensity. Our AI 
tutor network will construct an optimized academic calendar tailored directly to you.
</p>
</div>
""", unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            subject = st.text_input(":material/school: Focus Course / Subtopics:", placeholder="e.g., 'Unit 3 Computer Graphics', 'Java Programming'...")
            pace = st.select_slider(":material/speed: Study Pace Intensity:", options=["Relaxed (Steady)", "Balanced (Recommended)", "Intense (Cram Mode)"], value="Balanced (Recommended)")
        
        with col2:
            timeframe = st.selectbox(":material/event: Target Duration:", options=["1 Week Schedule", "2 Week Roadmap", "4 Week Intensive Mastery"], index=0)
            daily_hrs = st.slider(":material/hourglass_empty: Daily Target Hours:", min_value=1, max_value=8, value=3)

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        
        if st.button("🚀 Generate Personalized Blueprint", type="primary", use_container_width=True, icon=":material/calendar_month:", disabled=bool(st.session_state.planner_task_id)):
            with st.spinner("Querying context parameters..."):
                # Fetch context
                vector_store = VectorStore()
                search_query = subject if subject.strip() else "Syllabus Outline Chapter Topics"
                context_chunks = vector_store.search(search_query, top_k=5)
                context_str = "\n---\n".join(context_chunks) if context_chunks else ""
                context_str = context_str[:3500]

            task_desc = (
                f"Create an academic study plan for '{subject if subject.strip() else 'Uploaded Material'}'. "
                f"Covering a duration of {timeframe}. Intensity chosen: {pace}. "
                f"Target daily commitment: {daily_hrs} hours per day. "
                f"Include explicit breakdowns for each day and a comprehensive, aligned Markdown Timetable."
            )

            topic_title = subject.strip() if subject.strip() else "Personalized Study Schedule"
            
            # SPAWN BACKGROUND QUEUE TASK
            task_id = start_background_task("planner", topic_title, run_study_crew, task_desc, "plan", context_str)
            st.session_state.planner_task_id = task_id
            st.rerun()

    # --- ACTIVE VIEW PHASE ---
    else:
        st.markdown("""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;'>
            <h2 style='margin: 0; color: var(--dark-indigo); display:flex; align-items:center; gap:8px;'>
                <span class="material-icons-round" style="color: #7C3AED;">event_available</span> Active Study Blueprint
            </h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='blueprint-container'>", unsafe_allow_html=True)
        
        # Render generated plan (which now enforces GFM tables)
        st.markdown(st.session_state.plan_content)
        
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🔄 Create a New Schedule", type="primary", use_container_width=True, icon=":material/restart_alt:"):
            st.session_state.plan_active = False
            st.session_state.plan_content = ""
            st.rerun()
