"""
Vision Tool
"""

from typing import Optional
from PIL import Image

def process_image(uploaded_file) -> Optional[Image.Image]:
    try:
        image = Image.open(uploaded_file)
        image.verify()
        uploaded_file.seek(0)
        return Image.open(uploaded_file)
    except Exception:
        return None
