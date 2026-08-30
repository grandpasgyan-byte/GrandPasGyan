"""
GrandPa's Gyan - Configuration Engine
Manages API keys and environment parameters securely.
"""

import os
import streamlit as st

# Valid production Gemini models
DEFAULT_MODEL = "gemini-2.5-flash"
FALLBACK_MODELS = ["gemini-2.0-flash", "gemini-1.5-flash"]
MAX_DIRECT_PDF_SIZE = 10 * 1024 * 1024  # 10 MB limit for inline parsing

# Hardcoded fallback (Must start with 'AIzaSy...')
SET_API_KEY = ""

def get_api_key() -> str:
    """Retrieves Gemini API Key securely from Streamlit Secrets, Environment, or Config."""
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
        key = st.secrets["GEMINI_API_KEY"]
        if key:
            return key

    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key

    return SET_API_KEY
