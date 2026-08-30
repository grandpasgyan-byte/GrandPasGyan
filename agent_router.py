"""
GrandPa's Gyan - Intent Router
"""

import re
from typing import Dict, Any
from agents_registry import AGENTS_DATABASE

def route_agent_automatically(user_query: str, current_agent_name: str) -> str:
    query_lower = user_query.lower()
    
    for name, config in AGENTS_DATABASE.items():
        keywords = config.get("keywords", [])
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, query_lower):
                return name
                
    return current_agent_name

def get_agent_config(agent_name: str) -> Dict[str, Any]:
    return AGENTS_DATABASE.get(agent_name, AGENTS_DATABASE["GrandPa General Tutor"])
