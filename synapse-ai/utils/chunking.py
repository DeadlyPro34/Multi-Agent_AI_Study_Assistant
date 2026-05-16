from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_text_chunks(text, chunk_size=1000, chunk_overlap=200):
    """
    Splits the extracted text into manageable chunks for embeddings.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks
