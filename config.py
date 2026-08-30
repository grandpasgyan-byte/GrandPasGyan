"""
GrandPa's Gyan - Configuration Engine
Manages API keys and environment parameters securely.
"""

import os
import streamlit as st

DEFAULT_MODEL = "gemini-3.6-flash"
FALLBACK_MODELS = ["gemini-3.5-flash", "gemini-2.5-flash", "gemini-2.0-flash"]
MAX_DIRECT_PDF_SIZE = 10 * 1024 * 1024  # 10 MB limit for inline parsing

# Configured Gemini API Key
SET_API_KEY = "AQ.Ab8RN6J_JERm99cKUtN_-ZpFB4N4vRCEXzQ1ZqUQHWWEsGspwA"

def get_api_key() -> str:
    """Retrieves Gemini API Key from hardcoded value, Streamlit Secrets, or Environment Variables."""
    if SET_API_KEY:
        return SET_API_KEY
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and hasattr(st, "secrets"):
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    return api_key
