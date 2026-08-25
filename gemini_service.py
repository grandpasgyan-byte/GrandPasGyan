"""
GrandPa's Gyan - Gemini API Service Interface
"""

from typing import List, Optional, Any, Generator
from google import genai
from google.genai import types
from google.genai.errors import APIError
from config import DEFAULT_MODEL, get_api_key

def get_client() -> genai.Client:
    key = get_api_key()
    if not key:
        raise ValueError("Missing Gemini API Key.")
    return genai.Client(api_key=key)

def stream_gemini_response(
    system_instruction: str,
    user_prompt: str,
    attachments: Optional[List[Any]] = None,
    use_search: bool = False,
    model_name: str = DEFAULT_MODEL
) -> Generator[str, None, None]:
    """
    Streams response text chunk-by-chunk for real-time UI rendering.
    """
    client = get_client()
    contents = [user_prompt]
    
    if attachments:
        contents.extend(attachments)

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.4,
    )
    
    if use_search:
        config.tools = [{"google_search": {}}]

    try:
        response_stream = client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=config,
        )
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text

    except APIError as e:
        yield f"\n\n**API Error:** {getattr(e, 'message', str(e))}"
    except Exception as e:
        yield f"\n\n**Error:** {str(e)}"
