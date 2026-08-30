"""
GrandPa's Gyan - Visual Mind Map Generator
Generates Markdown visual tree representations.
"""

def generate_mindmap_markdown(concept: str) -> str:
    """Generates ASCII visual tree representation for concepts."""
    return f"""
```text
{concept.upper()}
 ├── 1. Core Definition & Principles
 │    ├── Primary Concepts
 │    └── Governing Laws & Formulas
 ├── 2. Practical Applications
 │    ├── Numerical Problems
 │    └── Real-world Examples
 └── 3. Exam Focus Areas
      ├── Common Misconceptions
      └── High-Yield Questions
