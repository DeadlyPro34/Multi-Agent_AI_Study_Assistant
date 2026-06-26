import streamlit as st
from utils.memory import get_conversation_history, add_message
from utils.rag_pipeline import VectorStore
from agents.crew_setup import run_study_crew

from utils.async_manager import start_background_task, check_task_status

@st.fragment(run_every=1.5)
def auto_poll_chat():
    if st.session_state.get("chat_task_id"):
        task = check_task_status(st.session_state.chat_task_id)
        if task and task["status"] in ["COMPLETED", "FAILED"]:
            st.rerun()


def render_chat_ui(agent_mode="explain"):
    st.markdown(f"### 💬 SynapseAI Assistant - Mode: {agent_mode.capitalize()}")
    
    if "chat_task_id" not in st.session_state:
        st.session_state.chat_task_id = None

    # --- POLLING FOR ACTIVE BACKGROUND CHAT TASK ---
    if st.session_state.chat_task_id:
        task = check_task_status(st.session_state.chat_task_id)
        if task:
            if task["status"] == "COMPLETED":
                add_message("assistant", task["result"])
                st.session_state.chat_task_id = None
                st.rerun()
            elif task["status"] == "FAILED":
                add_message("assistant", f"⚠️ Error: {task['result']}")
                st.session_state.chat_task_id = None
                st.rerun()

    history = get_conversation_history()
    
    # Display clean start screen if no messages exist
    if not history:
        st.markdown("""
<div class='glass-card' style='padding: 36px; text-align: center; margin-top: 2rem; margin-bottom: 2.5rem;'>
<span class="material-icons-round" style='font-size: 3.5rem; background: linear-gradient(135deg, #4F46E5, #7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; display: inline-block;'>forum</span>
<h2 style='margin-top:0; color: var(--dark-indigo); font-size: 1.75rem;'>SynapseAI Academic Intelligence Chat</h2>
<p style='color: var(--text-secondary); font-size: 0.95rem; max-width: 500px; margin: 0 auto 1.5rem;'>
Ask complex questions, dissect formulas, or seek step-by-step guides from your uploaded knowledge base documents.
</p>
<div style='display: flex; gap: 16px; justify-content: center; margin-top: 24px; text-align: left;'>
<div style='flex: 1; background: rgba(79, 70, 229, 0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(79, 70, 229, 0.1); font-size: 0.85rem; min-height: 90px;'>
<strong style="color: var(--primary-indigo); display: block; margin-bottom: 6px; font-size: 0.9rem;">💡 Conceptual Analysis</strong>
"Provide an analogy to understand how [Topic] operates in the notes."
</div>
<div style='flex: 1; background: rgba(79, 70, 229, 0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(79, 70, 229, 0.1); font-size: 0.85rem; min-height: 90px;'>
<strong style="color: var(--primary-indigo); display: block; margin-bottom: 6px; font-size: 0.9rem;">🧩 Fact Lookup & Synthesis</strong>
"What are the main differences between concepts described in Chapter 2?"
</div>
</div>
</div>
""", unsafe_allow_html=True)
    else:
        # Display chat messages from history on app rerun
        for message in history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Display "Typing" status if a background task is active
    if st.session_state.chat_task_id:
        with st.chat_message("assistant"):
            st.markdown("""
            <div style='display: flex; flex-direction: column; gap: 12px;'>
                <div style='display: flex; align-items: center; gap: 12px;'>
                    <div class="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                    <div style='color: var(--text-secondary); font-size: 0.95rem; font-weight: 500; letter-spacing: -0.01em;'>
                        SynapseAI is formulating a response...
                    </div>
                </div>
                <div style='max-width: 200px;'>
                    <!-- The Streamlit button will be rendered below this HTML block -->
                </div>
            </div>
            
            <style>
            .typing-indicator {
                display: flex;
                align-items: center;
                gap: 4px;
                background: rgba(79, 70, 229, 0.08);
                padding: 8px 12px;
                border-radius: 16px;
                width: fit-content;
            }
            .typing-indicator span {
                width: 6px;
                height: 6px;
                background-color: var(--primary-indigo);
                border-radius: 50%;
                opacity: 0.4;
                animation: bounce 1.4s infinite ease-in-out both;
            }
            .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
            .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
            
            @keyframes bounce {
                0%, 80%, 100% { transform: scale(0); opacity: 0.4; }
                40% { transform: scale(1.0); opacity: 1; }
            }
            </style>
            """, unsafe_allow_html=True)
            st.button("🔄 Sync Live Reply", key="sync_chat_manual", use_container_width=False, help="Click to check if the AI has finished generating")

    # Accept user input
    if not st.session_state.chat_task_id:
        if prompt := st.chat_input(f"Ask the {agent_mode} agent..."):
            add_message("user", prompt)
            with st.chat_message("user"):
                st.markdown(prompt)

            # Determine Context
            with st.spinner("Analyzing context..."):
                if st.session_state.chat_task_id:
                    st.warning("A task is already running. Please wait.")
                    st.stop()
                
                is_greeting = prompt.strip().lower().rstrip('.?!') in ["hi", "hello", "hey", "greetings", "yo", "hello there", "howdy", "hola"]
                if is_greeting:
                    context_str = "[SPECIAL MODE]: The user is just saying hello. Greet them warmly as SynapseAI."
                else:
                    vector_store = VectorStore()
                    context_chunks = vector_store.search(prompt, top_k=5)
                    context_str = "\n---\n".join(context_chunks) if context_chunks else "No specific context found."
                    context_str = context_str[:3500]
            
            # Spawn Async Task
            task_title = prompt[:30] + "..." if len(prompt) > 30 else prompt
            chat_history = st.session_state.get("messages", [])
            task_id = start_background_task("chat", task_title, run_study_crew, prompt, agent_mode, context_str, chat_history)
            st.session_state.chat_task_id = task_id
            st.rerun()

    # Automatically poll if a task is running to avoid manual clicking
    if st.session_state.chat_task_id:
        auto_poll_chat()
