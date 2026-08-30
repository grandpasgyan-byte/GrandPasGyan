"""
GrandPa's Gyan - Configuration Engine
Manages API keys and environment parameters securely.
"""

import os
import streamlit as st

DEFAULT_MODEL = "gemini-2.5-flash"
FALLBACK_MODELS = ["gemini-2.0-flash", "gemini-1.5-flash"]
MAX_DIRECT_PDF_SIZE = 10 * 1024 * 1024  # 10 MB limit for inline parsing

# Optional hardcoded fallback key (MUST start with 'AIzaSy...')
SET_API_KEY = ""

def get_api_key() -> str:
    """Retrieves Gemini API Key securely from Streamlit Secrets, Environment, or Config."""
    # 1. Check Streamlit Secrets
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        key = st.secrets["GEMINI_API_KEY"]
        if key:
            return key

    # 2. Check Environment Variables
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key

    # 3. Check hardcoded key
    return SET_API_KEY
