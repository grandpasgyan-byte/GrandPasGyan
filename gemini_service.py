"""
GrandPa's Gyan - Gemini AI Service Interface
Handles streaming responses, fallback handling, multimodal payloads, web grounding, and AST calculator intercepts.
"""

from typing import List, Optional, Any, Generator
from google import genai
from google.genai import types
from google.genai.errors import APIError
from config import DEFAULT_MODEL, FALLBACK_MODELS, get_api_key
from tools.web_search import extract_citations
from tools.calculator import evaluate_expression

def get_client() -> genai.Client:
    """Returns an authenticated Google GenAI client instance."""
    api_key = get_api_key()
    if not api_key:
        raise ValueError("Gemini API Key is missing. Please configure your key in Streamlit Secrets.")
    return genai.Client(api_key=api_key)

def stream_gemini_response(
    system_instruction: str,
    user_prompt: str,
    attachments: Optional[List[Any]] = None,
    file_doc: Optional[Any] = None,
    tools_list: Optional[List[str]] = None,
    model_name: str = DEFAULT_MODEL
) -> Generator[str, None, None]:
    """Streams response content dynamically while supporting Web Search & Calculator integration."""
    try:
        client = get_client()
    except Exception as e:
        yield f"⚠️ Client Initialization Error: {str(e)}"
        return

    if tools_list and "calculator" in tools_list and user_prompt.startswith("="):
        calc_result = evaluate_expression(user_prompt[1:])
        if calc_result is not None:
            yield f"**AST Direct Calculation Result:** `{calc_result}`\n\n"

    contents = []
    if file_doc:
        contents.append(file_doc)
    if attachments:
        contents.extend(attachments)
    contents.append(user_prompt)

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.4,
    )

    if tools_list and "google_search" in tools_list:
        config.tools = [{"google_search": {}}]

    models_to_try = [model_name] + [m for m in FALLBACK_MODELS if m != model_name]

    for current_model in models_to_try:
        try:
            response_stream = client.models.generate_content_stream(
                model=current_model,
                contents=contents,
                config=config
            )

            last_chunk = None
            for chunk in response_stream:
                last_chunk = chunk
                if chunk.text:
                    yield chunk.text

            if tools_list and "google_search" in tools_list and last_chunk:
                citations = extract_citations(last_chunk)
                if citations:
                    yield citations

            return

        except APIError as e:
            err_msg = str(e)
            if "RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg or "quota" in err_msg.lower():
                if current_model != models_to_try[-1]:
                    yield f"*(Quota limit on `{current_model}`. Switching to fallback model...)*\n\n"
                    continue
            yield f"\n\n⚠️ **API Error:** You have exceeded your rate limits on Google AI Studio. Please create a new project API key or wait for the quota window to reset."
            return
        except Exception as e:
            yield f"\n\n⚠️ **Execution Error:** {str(e)}"
            return
