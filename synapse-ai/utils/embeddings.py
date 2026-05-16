import streamlit as st
from sentence_transformers import SentenceTransformer

@st.cache_resource
def get_embedding_model():
    """
    Load the sentence transformer model for embeddings.
    Cached so it's not reloaded on every run.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def generate_embeddings(text_list):
    """
    Generate embeddings for a list of text chunks.
    """
    model = get_embedding_model()
    embeddings = model.encode(text_list, show_progress_bar=False)
    return embeddings.tolist()
