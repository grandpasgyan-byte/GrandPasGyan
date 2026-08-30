"""
GrandPa's Gyan - Curriculum Knowledge & RAG Retrieval Engine
Retrieves indexed textbook context for CBSE / NCERT alignment.
"""

from typing import List, Dict

LOCAL_NCERT_KNOWLEDGE: List[Dict[str, str]] = [
    {
        "grade": "Class 10",
        "subject": "Science",
        "chapter": "Chemical Reactions and Equations",
        "content": "A chemical reaction breaks and forms bonds. Types: Combination, Decomposition, Displacement, Double Displacement, Redox. Balancing obeys Conservation of Mass."
    },
    {
        "grade": "Class 10",
        "subject": "Mathematics",
        "chapter": "Quadratic Equations",
        "content": "Standard form: ax^2 + bx + c = 0 (a != 0). Quadratic formula: x = (-b ± sqrt(b^2 - 4ac)) / (2a). Discriminant D = b^2 - 4ac determines roots."
    },
    {
        "grade": "Class 10",
        "subject": "Science",
        "chapter": "Light - Reflection & Refraction",
        "content": "Snell's Law: sin(i)/sin(r) = constant (Refractive Index). Mirror formula: 1/f = 1/v + 1/u. Lens formula: 1/f = 1/v - 1/u. Power P = 1/f (in meters)."
    },
    {
        "grade": "Class 12",
        "subject": "Physics",
        "chapter": "Electric Charges and Fields",
        "content": "Coulomb's Law: F = k*(q1*q2)/r^2. Gauss's Law: Total electric flux through a closed surface equals net enclosed charge divided by epsilon_0."
    }
]

def retrieve_curriculum_context(query: str, grade: str = "Class 10", subject: str = "Science") -> str:
    """Retrieves matching curriculum snippets to enforce textbook accuracy."""
    query_lower = query.lower()
    retrieved_blocks = []

    for item in LOCAL_NCERT_KNOWLEDGE:
        if item["grade"].lower() == grade.lower():
            words = [w for w in query_lower.split() if len(w) > 3]
            if any(w in item["content"].lower() or w in item["chapter"].lower() for w in words):
                retrieved_blocks.append(f"[{item['chapter']}]: {item['content']}")

    if not retrieved_blocks:
        return "Align all explanations strictly with NCERT / Board textbook guidelines."

    return "\n".join(retrieved_blocks)
