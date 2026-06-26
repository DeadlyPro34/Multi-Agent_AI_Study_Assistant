import os
import uuid
import chromadb
from utils.embeddings import generate_embeddings
import streamlit as st

# Setup ChromaDB local storage
persist_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "chroma_db")
os.makedirs(persist_directory, exist_ok=True)

class VectorStore:
    def __init__(self, collection_name=None):
        if not collection_name:
            from streamlit.runtime.scriptrunner import get_script_run_ctx
            ctx = get_script_run_ctx()
            session_id = ctx.session_id if ctx else "default"
            collection_name = f"synapse_{session_id}"
            
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_chunks(self, chunks):
        """Embed and add text chunks to the ChromaDB collection."""
        if not chunks:
            return
        embeddings = generate_embeddings(chunks)
        ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
        self.collection.add(embeddings=embeddings, documents=chunks, ids=ids)

    def search(self, query, top_k=2):
        """Search for top_k most similar chunks to the query."""
        if self.collection.count() == 0:
            return []
        query_embedding = generate_embeddings([query])[0]
        results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        if results and "documents" in results and results["documents"]:
            return results["documents"][0]
        return []

    def clear(self):
        """Fully purge and recreate the ChromaDB collection to guarantee a clean reset."""
        try:
            name = self.collection.name
            self.client.delete_collection(name)
            self.collection = self.client.get_or_create_collection(name=name)
        except Exception as e:
            print(f"Error during complete collection purge: {e}")
            try:
                all_data = self.collection.get(limit=10000)
                if all_data and "ids" in all_data and all_data["ids"]:
                    self.collection.delete(ids=all_data["ids"])
            except:
                pass

def get_vectorstore():
    """Returns a VectorStore instance cached in the current user's session."""
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = VectorStore()
    return st.session_state.vector_store
