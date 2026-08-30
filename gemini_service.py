"""
Gemini Service - AI Model Integration
Updated for Gemini 3.6 Flash
"""

import os
import streamlit as st
from google import genai
from google.genai import types

def get_client():
    """Retrieves authenticated Gemini Client."""
    api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def stream_gemini_response(system_instruction, user_prompt, attachments=None, file_doc=None, tools_list=None):
    """Streams responses from Google Gemini API using gemini-3.6-flash model."""
    client = get_client()
    if not client:
        yield "⚠️ API key is missing. Please provide a valid Gemini API Key."
        return

    # UPDATED TO GEMINI 3.6 FLASH
    MODEL_NAME = "gemini-3.6-flash"

    contents = []
    
    if file_doc:
        contents.append(file_doc)
        
    if attachments:
        contents.extend(attachments)
        
    contents.append(user_prompt)

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.7,
    )

    try:
        response = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=contents,
            config=config
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"API Error: {str(e)}"
