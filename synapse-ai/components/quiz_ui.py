import streamlit as st
import json
import re
from utils.rag_pipeline import VectorStore
from agents.crew_setup import run_study_crew

def extract_json_quiz(text):
    """
    Safely extracts and parses JSON quiz data from LLM string response.
    """
    try:
        # Try parsing directly first
        return json.loads(text.strip())
    except:
        pass
        
    try:
        # Look for ```json ... ``` blocks
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL | re.IGNORECASE)
        if match:
            return json.loads(match.group(1))
    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON parsing error (block match): {e}")

    try:
        # Last resort: find text between first { and last }
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON parsing error (braces match): {e}")
        
    return None

from utils.async_manager import start_background_task, check_task_status

@st.fragment(run_every=1.5)
def auto_poll_quiz():
    if st.session_state.get("quiz_task_id"):
        task = check_task_status(st.session_state.quiz_task_id)
        if task:
            if task["status"] == "COMPLETED":
                response_text = task["result"]
                quiz_data = extract_json_quiz(response_text)
                if quiz_data and "questions" in quiz_data and len(quiz_data["questions"]) > 0:
                    st.session_state.quiz_questions = quiz_data["questions"]
                    st.session_state.quiz_active = True
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_user_answers = {}
                    st.session_state.quiz_task_id = None
                    st.rerun()
                else:
                    st.error("❌ Failed to parse a valid quiz from the agent output. Please retry with a different topic.")
                    st.session_state.quiz_task_id = None
                    st.rerun()
            elif task["status"] == "FAILED":
                st.error(f"🚨 Quiz Generation Failed: {task['result']}")
                st.session_state.quiz_task_id = None
                st.rerun()

def render_quiz_ui():
    # Initialize session state variables for Quiz Mode
    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = False
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "quiz_user_answers" not in st.session_state:
        st.session_state.quiz_user_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_task_id" not in st.session_state:
        st.session_state.quiz_task_id = None


    if st.session_state.quiz_task_id:
        auto_poll_quiz()

    # Display custom UI Header
    st.markdown("""
    <style>
    .quiz-container {
        background: var(--bg-card);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    .quiz-question {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--dark-indigo);
        margin-bottom: 12px;
    }
    .result-card {
        padding: 16px;
        border-radius: 12px;
        margin-top: 12px;
    }
    .result-success {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgb(16, 185, 129);
        color: rgb(6, 95, 70);
    }
    .result-error {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgb(239, 68, 68);
        color: rgb(153, 27, 27);
    }
    .score-header {
        text-align: center;
        background: linear-gradient(135deg, var(--primary-indigo), var(--primary-lavender));
        color: white !important;
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

    # --- 0. ACTIVE BACKGROUND VIEW ---
    if st.session_state.quiz_task_id:
        st.markdown("""
<div class='glass-card' style='padding: 40px; text-align: center; margin-bottom: 2rem;'>
<div style='font-size: 3.5rem; margin-bottom: 1.5rem;'>📝🕵️‍♂️⚡</div>
<h2 style='margin-top:0; color: var(--dark-indigo);'>Crafting Your Custom Examination...</h2>
<p style='color: var(--text-secondary); font-size: 0.95rem; max-width: 600px; margin: 0 auto 1.5rem auto;'>
    The Strict Examiner Agent is currently cross-referencing your documents to generate high-fidelity questions.
</p>
<div style='background: rgba(79, 70, 229, 0.05); border: 1px dashed var(--primary-indigo); border-radius: 12px; padding: 16px; font-size: 0.9rem; color: var(--primary-indigo); font-weight: 500;'>
    ✨ Since this is running in the background, you can head over to <b>Summaries</b> or <b>Planner</b>!
    We will notify your <b>Header Bell</b> as soon as the test is ready.
</div>
</div>
""", unsafe_allow_html=True)
        with st.spinner("Examiner is analyzing document sectors..."):
            st.button("🔄 Refresh Quiz Status", use_container_width=True)

    # --- STAGE 1: QUIZ CONFIGURATION ---
    elif not st.session_state.quiz_active:
        st.markdown("""
<div class='glass-card' style='padding: 32px; text-align: center; margin-bottom: 2rem;'>
<span class="material-icons-round" style='font-size: 3.5rem; background: linear-gradient(135deg, #4F46E5, #7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; display: inline-block;'>school</span>
<h2 style='margin-top:0; color: var(--dark-indigo);'>Configure Your Premium Quiz</h2>
<p style='color: var(--text-secondary); font-size: 0.95rem; max-width: 600px; margin: 0 auto;'>
Select a topic from your study material, set your desired size, and let the AI 
strict examiner challenge your understanding.
</p>
</div>
""", unsafe_allow_html=True)

        # Form Layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            quiz_topic = st.text_input(":material/track_changes: Enter Specific Topic (e.g. 'Unit 3 3D Viewing' or leave empty for all materials):", 
                                     placeholder="Ex: 'Java Virtual Machine', 'AR/VR Applications'...")
            
        with col2:
            num_questions = st.slider(":material/format_list_numbered: Number of Questions:", min_value=3, max_value=10, value=5)
            difficulty = st.select_slider(":material/military_tech: Difficulty Level:", options=["Basic", "Intermediate", "Hard"], value="Intermediate")

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        
        if st.button("🚀 Generate Quiz", type="primary", use_container_width=True, icon=":material/quiz:", disabled=bool(st.session_state.quiz_task_id)):
            with st.spinner("Extracting parameters from knowledge base..."):
                vector_store = VectorStore()
                search_query = quiz_topic if quiz_topic.strip() else "Course Outline Syllabus Summary"
                context_chunks = vector_store.search(search_query, top_k=5)
                context_str = "\n---\n".join(context_chunks) if context_chunks else ""
                context_str = context_str[:3500]
                
            # 2. Formulate precise Prompt
            task_desc = (
                f"Generate a {difficulty} level quiz containing EXACTLY {num_questions} multiple choice questions. "
                f"Topic requested: {quiz_topic if quiz_topic.strip() else 'Comprehensive knowledge review'}. "
            )
            
            topic_title = quiz_topic.strip() if quiz_topic.strip() else "Full Knowledge Exam"
            
            # SPAWN BACKGROUND TASK
            task_id = start_background_task("quiz", topic_title, run_study_crew, task_desc, "quiz", context_str)
            st.session_state.quiz_task_id = task_id
            st.rerun()

    # --- STAGE 2: ACTIVE QUIZ SCREEN ---
    elif st.session_state.quiz_active and not st.session_state.quiz_submitted:
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;'>
            <h2 style='margin: 0; color: var(--dark-indigo); display:flex; align-items:center; gap:8px;'>
                <span class="material-icons-round" style="color: var(--primary-indigo);">edit_note</span> Live Examination
            </h2>
            <span style='background: var(--primary-indigo); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;'>
                {len(st.session_state.quiz_questions)} Questions Remaining
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        # Display Questions
        for idx, q in enumerate(st.session_state.quiz_questions):
            st.markdown(f"""
            <div class='quiz-container'>
                <div class='quiz-question'>Q{idx+1}. {q.get('question')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            options = q.get('options', [])
            
            # Key is dynamic to link to this specific question
            answer_key = f"q_{idx}"
            
            # Render standard selectbox/radio but custom
            choice = st.radio(
                label=f"Select Option for Q{idx+1}",
                options=options,
                index=None, # No default selection to force them to pick
                key=answer_key,
                label_visibility="collapsed"
            )
            
            # Save to state answers
            if choice is not None:
                st.session_state.quiz_user_answers[idx] = choice
                
            st.markdown("<br>", unsafe_allow_html=True)

        col_sub, col_reset = st.columns([3, 1])
        with col_sub:
            if st.button("🚀 Submit Exam", type="primary", use_container_width=True, icon=":material/check_circle:"):
                # Grade Answers
                correct_count = 0
                for idx, q in enumerate(st.session_state.quiz_questions):
                    user_choice = st.session_state.quiz_user_answers.get(idx)
                    correct_answer = q.get('answer')
                    
                    # Flex match (strip space, lowercase)
                    if user_choice and str(user_choice).strip().lower() == str(correct_answer).strip().lower():
                        correct_count += 1
                
                st.session_state.quiz_score = correct_count
                st.session_state.quiz_submitted = True
                st.rerun()
                
        with col_reset:
            if st.button("❌ Cancel Quiz", use_container_width=True):
                st.session_state.quiz_active = False
                st.rerun()

    # --- STAGE 3: RESULTS SCREEN ---
    elif st.session_state.quiz_submitted:
        score_pct = int((st.session_state.quiz_score / len(st.session_state.quiz_questions)) * 100)
        
        st.markdown(f"""
        <div class='score-header'>
            <h1 style='color: white; margin: 0; font-size: 2.5rem;'>📊 Exam Result</h1>
            <p style='margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9;'>You scored <strong>{st.session_state.quiz_score}</strong> out of <strong>{len(st.session_state.quiz_questions)}</strong></p>
            <div style='font-size: 3rem; font-weight: 800; margin-top: 15px;'>{score_pct}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Individual Feedback List
        for idx, q in enumerate(st.session_state.quiz_questions):
            user_choice = st.session_state.quiz_user_answers.get(idx, "No response provided")
            correct_answer = q.get('answer')
            explanation = q.get('explanation', 'No explanation available.')
            
            is_correct = str(user_choice).strip().lower() == str(correct_answer).strip().lower()
            
            feedback_class = "result-success" if is_correct else "result-error"
            icon = "✅" if is_correct else "❌"
            
            correct_answer_html = f"<p>Correct Answer: <strong style='color: #10B981;'>{correct_answer}</strong></p>" if not is_correct else ""
            
            st.markdown(f"""
            <div class='quiz-container'>
                <div class='quiz-question'>Q{idx+1}. {q.get('question')}</div>
                <div style='margin-left: 12px; font-size: 0.95rem;'>
                    <p>Your Answer: <strong style='color: {"#10B981" if is_correct else "#EF4444"};'>{user_choice}</strong> {icon}</p>
                    {correct_answer_html}
                </div>
                <div class='result-card {feedback_class}'>
                    <strong>💡 Explanation:</strong> {explanation}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔄 Take Another Quiz", type="primary", use_container_width=True, icon=":material/replay:"):
            # Reset all
            st.session_state.quiz_active = False
            st.session_state.quiz_questions = []
            st.session_state.quiz_user_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()
