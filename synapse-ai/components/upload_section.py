import streamlit as st
from utils.pdf_reader import extract_text_from_pdfs
from utils.chunking import get_text_chunks
from utils.rag_pipeline import VectorStore

def render_upload_section():
    st.markdown("""
    <h3 style="display: flex; align-items: center; gap: 10px; color: var(--dark-indigo); margin-bottom: 8px; margin-top: 0;">
        <span class="material-icons-round" style="color: var(--primary-indigo); font-size: 1.8rem;">cloud_upload</span>
        Upload Knowledge Base
    </h3>
    """, unsafe_allow_html=True)
    st.markdown("Upload your textbooks, slides, and notes (PDF) here to give SynapseAI context.")
    
    pdf_docs = st.file_uploader("Drop your PDFs here", accept_multiple_files=True, type=["pdf"])
    
    if st.button("Process Documents", type="primary", icon=":material/rocket_launch:"):
        if pdf_docs:
            with st.spinner("Analyzing and encoding documents... ⏳"):
                # Extract text
                raw_text = extract_text_from_pdfs(pdf_docs)
                
                # Chunking
                text_chunks = get_text_chunks(raw_text)
                
                # Embedding and Storing
                vector_store = VectorStore()
                # Optional: clear previous docs if you want a fresh DB per session
                # vector_store.clear() 
                vector_store.add_chunks(text_chunks)
                
                st.success(f"Successfully processed {len(pdf_docs)} document(s) into {len(text_chunks)} chunks! SynapseAI is ready.")
        else:
            st.warning("Please upload at least one PDF.")
