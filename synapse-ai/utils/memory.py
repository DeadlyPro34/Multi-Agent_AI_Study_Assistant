import streamlit as st

def get_conversation_history():
    """
    Retrieve conversation history from session state.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    return st.session_state.messages

def add_message(role, content):
    """
    Add a new message to the conversation history.
    """
    st.session_state.messages.append({"role": role, "content": content})

def clear_memory():
    """
    Clear conversation history and purge the ChromaDB knowledge base.
    """
    st.session_state.messages = []
    
    # Clean Vector Store database
    try:
        from utils.rag_pipeline import get_vectorstore
        vector_store = get_vectorstore()
        vector_store.clear()
    except Exception as e:
        print(f"Error clearing vector store: {e}")
