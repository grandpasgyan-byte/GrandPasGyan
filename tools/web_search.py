"""
Web Search Tool metadata helper
"""

def is_search_enabled(agent_config: dict) -> bool:
    return "google_search" in agent_config.get("tools", [])
