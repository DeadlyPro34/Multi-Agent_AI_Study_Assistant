import sys
import os

# Set up path to ensure imports work correctly
sys.path.insert(0, os.path.abspath('.'))

from utils.pdf_reader import extract_text_from_pdfs
from utils.chunking import get_text_chunks
from utils.rag_pipeline import VectorStore

class MockUploadedFile:
    def __init__(self, filepath):
        self.file = open(filepath, 'rb')
        self.name = os.path.basename(filepath)
    
    def read(self, *args):
        return self.file.read(*args)
        
    def seek(self, *args):
        return self.file.seek(*args)
        
    def tell(self, *args):
        return self.file.tell(*args)

    def close(self):
        self.file.close()

def run_test():
    try:
        print("1. Opening PDF...")
        pdf_file = MockUploadedFile("Operating_Systems_and_DBMS_Concepts.pdf")
        
        print("2. Extracting text...")
        raw_text = extract_text_from_pdfs([pdf_file])
        print(f"Extracted {len(raw_text)} characters.")
        
        print("3. Chunking text...")
        chunks = get_text_chunks(raw_text)
        print(f"Created {len(chunks)} chunks.")
        
        print("4. Initializing VectorStore and adding chunks...")
        vector_store = VectorStore()
        # Make sure to clear it for the test
        vector_store.clear()
        vector_store.add_chunks(chunks)
        
        print("5. Testing retrieval...")
        result = vector_store.search("deadlock")
        if result:
            print(f"Success! Retrieved {len(result)} characters of context for 'deadlock'.")
        else:
            print("Failed to retrieve context.")
            
        print("PIPELINE TEST PASSED SUCCESSFULLY!")
        
    except Exception as e:
        import traceback
        print(f"PIPELINE TEST FAILED: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    run_test()
