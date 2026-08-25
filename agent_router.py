"""
GrandPa's Gyan - Intent Router Module
"""

import re
from typing import Dict, Any
from agents_registry import AGENTS_DATABASE

def route_agent_automatically(user_query: str, current_agent_name: str) -> str:
    """
    Scans user query for keywords to auto-route to a specialized agent.
    Defaults to current_agent_name if no keyword matches.
    """
    query_lower = user_query.lower()
    
    for name, config in AGENTS_DATABASE.items():
        keywords = config.get("keywords", [])
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, query_lower):
                return name
                
    return current_agent_name

def get_agent_config(agent_name: str) -> Dict[str, Any]:
    """Retrieves the configuration dictionary for a given agent name."""
    return AGENTS_DATABASE.get(agent_name, AGENTS_DATABASE.get("GrandPa General Tutor", {}))
