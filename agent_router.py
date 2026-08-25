"""
GrandPa's Gyan - Intent Router
Uses regex pattern matching with LLM classification backup to map queries to agents.
"""

import re
from typing import Dict, Any
from agents_registry import AGENTS_DATABASE

def route_agent_automatically(user_query: str, current_agent_name: str) -> str:
    """
    Determines if user input targets a specific specialized agent based on keywords.
    If no regex match occurs, returns the currently selected UI agent.
    """
    query_lower = user_query.lower()
    
    # 1. Direct Regex Keyword Match
    for name, config in AGENTS_DATABASE.items():
        keywords = config.get("keywords", [])
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, query_lower):
                return name
                
    # 2. Fallback to manually selected sidebar agent
    return current_agent_name

def get_agent_config(agent_name: str) -> Dict[str, Any]:
    """Retrieves config dictionary for target agent name."""
    return AGENTS_DATABASE.get(agent_name, AGENTS_DATABASE["GrandPa General Tutor"])
