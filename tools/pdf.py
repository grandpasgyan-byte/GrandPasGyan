"""
PDF RAG Tool
Extracts document text using PyPDF2 for small files or uploads to Gemini File API for large files.
"""

from typing import Optional, Tuple
import PyPDF2
from config import MAX_DIRECT_PDF_SIZE

def process_pdf_document(uploaded_file, client=None) -> Tuple[Optional[str], Optional[Any]]:
    """
    Intelligently routes PDF inputs:
    - Text extraction for files < 10 MB
    - Native Gemini File object for files >= 10 MB
    """
    file_bytes = uploaded_file.getvalue()
    file_size = len(file_bytes)
    
    if file_size < MAX_DIRECT_PDF_SIZE:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            extracted_text = ""
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted_text += f"\n--- [Page {i+1}] ---\n{text}"
            return extracted_text.strip() if extracted_text else None, None
        except Exception:
            return None, None
    else:
        # File API Route for Large Documents (> 10 MB)
        if client:
            try:
                uploaded_doc = client.files.upload(
                    file=uploaded_file,
                    mime_type="application/pdf"
                )
                return None, uploaded_doc
            except Exception:
                return None, None
        return None, None
