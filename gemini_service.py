"""
GrandPa's Gyan - Gemini API Service Interface
Manages model calls using the google-genai SDK, supporting streaming, vision, and tool grounding.
"""

from typing import List, Optional, Any, Generator
from google import genai
from google.genai import types
from google.genai.errors import APIError
from config import DEFAULT_MODEL, get_api_key
from tools.web_search import extract_citations
from tools.calculator import evaluate_expression

def get_client() -> genai.Client:
    """Instantiates Gemini API client."""
    key = get_api_key()
    if not key:
        raise ValueError("Gemini API key is not configured.")
    return genai.Client(api_key=key)

def stream_gemini_response(
    system_instruction: str,
    user_prompt: str,
    attachments: Optional[List[Any]] = None,
    file_doc: Optional[Any] = None,
    tools_list: Optional[List[str]] = None,
    model_name: str = DEFAULT_MODEL
) -> Generator[str, None, None]:
    """
    Streams content from Gemini API back to the UI, applying tools where requested.
    """
    client = get_client()
    contents = []
    
    # Check if prompt contains math calculation request
    if tools_list and "calculator" in tools_list and user_prompt.startswith("="):
        calc_result = evaluate_expression(user_prompt[1:])
        if calc_result is not None:
            yield f"**Calculation Result:** `{calc_result}`\n\n"
            
    contents.append(user_prompt)
    
    if attachments:
        contents.extend(attachments)
        
    if file_doc:
        contents.append(file_doc)

    # Configure Google Search Grounding tool if specified
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.3,
    )
    
    if tools_list and "google_search" in tools_list:
        config.tools = [{"google_search": {}}]

    try:
        response_stream = client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=config,
        )
        
        last_response = None
        for chunk in response_stream:
            last_response = chunk
            if chunk.text:
                yield chunk.text
                
        # Append Citations if Google Search Grounding was active
        if tools_list and "google_search" in tools_list and last_response:
            citations = extract_citations(last_response)
            if citations:
                yield citations

    except APIError as e:
        yield f"\n\n**API Error:** {getattr(e, 'message', str(e))}"
    except Exception as e:
        yield f"\n\n**System Error:** {str(e)}"
