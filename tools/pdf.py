"""
GrandPa's Gyan - PDF Extraction & Large File Tool
Parses small PDFs directly or routes large documents (>10MB) via File API.
"""

from typing import Optional, Tuple, Any
import PyPDF2
from config import MAX_DIRECT_PDF_SIZE

def process_pdf_document(uploaded_file, client=None) -> Tuple[Optional[str], Optional[Any]]:
    """Extracts text for small files or uploads large files to Gemini File API."""
    if not uploaded_file:
        return None, None

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
