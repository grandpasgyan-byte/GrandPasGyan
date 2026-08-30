"""
GrandPa's Gyan - Smart Intent Router
Routes user queries automatically using regex keyword boundary matching.
"""

import re
from typing import Dict, Any
from agents_registry import AGENTS_DATABASE

def route_agent_automatically(prompt: str, current_agent: str) -> str:
    """Routes user prompt based on keyword regex matching."""
    p = prompt.lower()

    for name, config in AGENTS_DATABASE.items():
        keywords = config.get("keywords", [])
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, p):
                return name

    return current_agent

def get_agent_config(agent_name: str) -> Dict[str, Any]:
    """Returns configuration dictionary for requested agent."""
    return AGENTS_DATABASE.get(agent_name, AGENTS_DATABASE["GrandPa General Tutor"])
