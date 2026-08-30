"""
Web Search & Citations Tool
"""

from typing import Any, List, Dict

def extract_citations(response: Any) -> str:
    citations_text = ""
    try:
        candidates = getattr(response, "candidates", [])
        if candidates:
            metadata = getattr(candidates[0], "grounding_metadata", None)
            chunks = getattr(metadata, "grounding_chunks", []) if metadata else []
            
            sources: List[Dict[str, str]] = []
            for chunk in chunks:
                web_data = getattr(chunk, "web", None)
                if web_data:
                    title = getattr(web_data, "title", "Web Source")
                    uri = getattr(web_data, "uri", "#")
                    sources.append({"title": title, "url": uri})
                    
            if sources:
                citations_text += "\n\n### 📚 Citations & Sources:\n"
                for src in sources:
                    citations_text += f"* [{src['title']}]({src['url']})\n"
    except Exception:
        pass
        
    return citations_text
