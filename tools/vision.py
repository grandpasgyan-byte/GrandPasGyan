"""
Vision & Image Processing Helper Tool
"""

from typing import Optional
from PIL import Image

def process_image(uploaded_file) -> Optional[Image.Image]:
    """Validates and loads image attachments into PIL objects."""
    try:
        image = Image.open(uploaded_file)
        image.verify()
        # Re-open after verify as per PIL requirement
        uploaded_file.seek(0)
        return Image.open(uploaded_file)
    except Exception:
        return None
