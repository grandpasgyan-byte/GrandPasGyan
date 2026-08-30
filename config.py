"""
GrandPa's Gyan - Configuration Engine
Manages API keys and environment parameters securely.
"""

import os
import streamlit as st

DEFAULT_MODEL = "gemini-3.6-flash"
FLASH_MODEL = "gemini-3.6-flash"
MAX_DIRECT_PDF_SIZE = 10 * 1024 * 1024  # 10 MB limit for inline parsing

def get_api_key() -> str:
    """Retrieves Gemini API Key from Streamlit Secrets or Environment Variables."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and hasattr(st, "secrets"):
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    return api_key
