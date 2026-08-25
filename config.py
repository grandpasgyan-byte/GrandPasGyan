"""
GrandPa's Gyan - Central Configuration
"""

import os
import streamlit as st

# Default Production Model (Gemini 3.6 Flash)
# Can be switched to "gemini-3.7-flash" for complex reasoning tasks
DEFAULT_MODEL = "gemini-3.6-flash"

# Retrieve API Key from Streamlit Secrets or Environment
def get_api_key() -> str:
    key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
    return key or ""
