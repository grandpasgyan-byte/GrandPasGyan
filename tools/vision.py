"""
Vision & Image Helper Tool
"""

from typing import Optional
from PIL import Image

def process_image(uploaded_file) -> Optional[Image.Image]:
    try:
        return Image.open(uploaded_file)
    except Exception:
        return None
