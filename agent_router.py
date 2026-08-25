"""
GrandPa's Gyan - Intent Router
"""

from typing import Dict, Any
from agents_registry import AGENTS_DATABASE

def route_agent(selected_agent_name: str) -> Dict[str, Any]:
    """
    Returns the agent configuration from registry.
    """
    return AGENTS_DATABASE.get(selected_agent_name, AGENTS_DATABASE["GrandPa General Tutor"])
