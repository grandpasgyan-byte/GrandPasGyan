"""
GrandPa's Gyan - Multilingual Voice TTS Engine
Converts text into in-memory MP3 audio streams using gTTS.
"""

import io
import re

def text_to_speech(text: str, lang_code: str = "English") -> io.BytesIO:
    """Converts response text into an in-memory MP3 audio buffer."""
    try:
        from gtts import gTTS
    except ImportError:
        from gTTS import gTTS

    clean_text = re.sub(r"[\*#_`~>\[\]\(\)]", "", text)
    clean_text = clean_text.strip()[:600]

    if not clean_text:
        clean_text = "Here is the response from GrandPa."

    lang_mapping = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te",
        "Tamil": "ta",
        "Kannada": "kn",
        "Marathi": "mr"
    }

    target_lang = lang_mapping.get(lang_code, "en")
    mp3_fp = io.BytesIO()
    tts = gTTS(text=clean_text, lang=target_lang, slow=False)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp
