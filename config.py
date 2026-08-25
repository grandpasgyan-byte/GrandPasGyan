"""
GrandPa's Gyan - Central Configuration Module
"""

import os
import streamlit as st

# Default Gemini Flash model for real-time educational tasks
DEFAULT_MODEL = "gemini-2.5-flash"

# Size threshold for local PDF text extraction vs. File API chunking (in bytes)
MAX_DIRECT_PDF_SIZE = 10 * 1024 * 1024  # 10 MB

def get_api_key() -> str:
    """Retrieves API key safely from Streamlit secrets or OS environment."""
    key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
    return key or ""
