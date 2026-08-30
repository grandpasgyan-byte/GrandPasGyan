"""
GrandPa's Gyan - Configuration Engine
Manages API keys and environment parameters securely.
"""

import os
import streamlit as st

DEFAULT_MODEL = "gemini-1.5-flash"
FALLBACK_MODELS = ["gemini-1.5-pro"]
MAX_DIRECT_PDF_SIZE = 10 * 1024 * 1024  # 10 MB limit for inline parsing

def get_api_key() -> str:
    """Retrieves Gemini API Key from Streamlit Secrets or Environment Variables."""
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        key = st.secrets["GEMINI_API_KEY"]
        if key:
            return key

    return os.environ.get("GEMINI_API_KEY", "")
