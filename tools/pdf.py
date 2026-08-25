"""
PDF Extraction Tool
"""

from typing import Optional
import PyPDF2

def extract_pdf_text(uploaded_file) -> Optional[str]:
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page_num, page in enumerate(reader.pages):
            extracted = page.extract_text()
            if extracted:
                text += f"\n--- [Page {page_num + 1}] ---\n{extracted}"
        return text.strip() if text else None
    except Exception:
        return None
