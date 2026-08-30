"""
Text-to-Speech (TTS) Voice Engine
"""

import io
from gTTS import gTTS

def text_to_speech(text: str, lang_code: str = "en") -> io.BytesIO:
    """Converts input response text into MP3 audio stream."""
    clean_text = text.replace("*", "").replace("#", "").strip()[:500]
    mp3_fp = io.BytesIO()
    tts = gTTS(text=clean_text if clean_text else "No audio available", lang=lang_code, slow=False)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp
