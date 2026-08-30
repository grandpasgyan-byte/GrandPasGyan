"""
GrandPa's Gyan - Quiz Engine & JSON Parser
"""

import json
from typing import List, Dict, Any

def parse_quiz_json(raw_text: str) -> List[Dict[str, Any]]:
    """Parses JSON quiz array from generated text."""
    try:
        start_idx = raw_text.find("[")
        end_idx = raw_text.rfind("]") + 1
        if start_idx != -1 and end_idx != -1:
            json_str = raw_text[start_idx:end_idx]
            return json.loads(json_str)
    except Exception:
        pass
    return []
