"""
GrandPa's Gyan - Image Vision Processor
Loads and validates image streams for homework analysis.
"""

from typing import Optional
from PIL import Image

def process_image(uploaded_file) -> Optional[Image.Image]:
    """Validates and opens uploaded image streams."""
    if not uploaded_file:
        return None
    try:
        image = Image.open(uploaded_file)
        image.verify()
        uploaded_file.seek(0)
        return Image.open(uploaded_file)
    except Exception:
        return None
