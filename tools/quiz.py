"""
Structured Quiz Generator Tool
Formats incoming practice questions and validates quiz structures.
"""

from typing import List, Dict, Any

def format_quiz_markdown(quiz_data: List[Dict[str, Any]]) -> str:
    """Formats a list of question dictionaries into clean markdown."""
    markdown_output = "### 📝 Practice Quiz\n\n"
    answer_key = "\n\n--- \n### 🔑 Answer Key & Explanations\n\n"
    
    for idx, item in enumerate(quiz_data, 1):
        markdown_output += f"**Question {idx}:** {item.get('question', '')}\n"
        options = item.get("options", [])
        for opt_idx, option in enumerate(options, 1):
            markdown_output += f"  - ({chr(64 + opt_idx)}) {option}\n"
        markdown_output += "\n"
        
        answer_key += f"**{idx}. Answer:** {item.get('correct_answer', '')}\n"
        answer_key += f"*Explanation:* {item.get('explanation', '')}\n\n"
        
    return markdown_output + answer_key
