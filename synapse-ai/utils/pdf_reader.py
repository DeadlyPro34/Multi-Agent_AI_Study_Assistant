import PyPDF2
import os
import re

def sanitize_extracted_text(text):
    """
    Cleans up extracted PDF text by repairing vertical word breaks caused by PDF rendering
    while preserving actual paragraph blocks.
    """
    if not text:
        return ""
        
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Split by paragraph breaks (sequences of whitespace with 2+ newlines)
    paragraphs = re.split(r'\n\s*\n', text)
    
    cleaned_paragraphs = []
    for para in paragraphs:
        # Collapse all nested newlines and extra horizontal spaces into single spaces
        cleaned_para = re.sub(r'\s+', ' ', para).strip()
        if cleaned_para:
            cleaned_paragraphs.append(cleaned_para)
            
    # Rejoin with clear double newlines
    return '\n\n'.join(cleaned_paragraphs)

def extract_text_from_pdfs(pdf_docs):
    """
    Extract text from a list of uploaded PDF files and run sanitization.
    """
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PyPDF2.PdfReader(pdf)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"Error reading {pdf.name}: {e}")
            
    # Return healed, fully semantic text
    return sanitize_extracted_text(text)
