"""
GrandPa's Gyan - Indian Curriculum Hierarchy Engine
Supports Board -> Grade -> Subject -> Chapter -> Topic mapping.
"""

from typing import Dict, List, Any

CURRICULUM_DATA: Dict[str, Any] = {
    "CBSE / NCERT": {
        "Class 10": {
            "Mathematics": {
                "Real Numbers": ["Euclid's Division Lemma", "Fundamental Theorem of Arithmetic", "Revisiting Irrational Numbers"],
                "Polynomials": ["Zeros of Polynomial", "Relationship between Zeros and Coefficients", "Division Algorithm"],
                "Quadratic Equations": ["Standard Form", "Solving by Factoring", "Quadratic Formula", "Nature of Roots"]
            },
            "Science": {
                "Chemical Reactions and Equations": ["Chemical Equations", "Types of Chemical Reactions", "Corrosion & Rancidity"],
                "Acids, Bases and Salts": ["Chemical Properties", "pH Scale", "Salts Spectrum"],
                "Life Processes": ["Nutrition", "Respiration", "Transportation", "Excretion"],
                "Light - Reflection & Refraction": ["Spherical Mirrors", "Refraction", "Lenses & Power"]
            },
            "English": {
                "Grammar & Usage": ["Idioms & Phrases", "Tenses", "Active/Passive Voice", "Direct/Indirect Speech"]
            }
        },
        "Class 12": {
            "Physics": {
                "Electric Charges and Fields": ["Coulomb's Law", "Electric Field Lines", "Electric Flux", "Gauss's Law"],
                "Electrostatic Potential": ["Equipotential Surfaces", "Potential Energy", "Capacitance"]
            },
            "Chemistry": {
                "Solutions": ["Types of Solutions", "Henry's Law", "Raoult's Law", "Colligative Properties"],
                "Electrochemistry": ["Nernst Equation", "Conductance", "Kohlrausch's Law"]
            }
        }
    },
    "AP / TS State Board": {
        "Class 10": {
            "Physical Science": {
                "Heat": ["Specific Heat", "Thermal Equilibrium", "Evaporation & Condensation"],
                "Chemical Reactions": ["Chemical Changes", "Exothermic & Endothermic Reactions"]
            }
        }
    },
    "ICSE": {
        "Class 10": {
            "Mathematics": {
                "Commercial Mathematics": ["GST", "Banking - Recurring Deposit"],
                "Algebra": ["Linear Inequations", "Matrices", "Arithmetic Progression"]
            },
            "Physics": {
                "Force, Work, Power & Energy": ["Turning Effect of Force", "Work Done", "Energy Conservation"]
            }
        }
    }
}

def get_boards() -> List[str]:
    return list(CURRICULUM_DATA.keys())

def get_grades(board: str) -> List[str]:
    return list(CURRICULUM_DATA.get(board, {}).keys())

def get_subjects(board: str, grade: str) -> List[str]:
    return list(CURRICULUM_DATA.get(board, {}).get(grade, {}).keys())

def get_chapters(board: str, grade: str, subject: str) -> List[str]:
    return list(CURRICULUM_DATA.get(board, {}).get(grade, {}).get(subject, {}).keys())

def get_topics(board: str, grade: str, subject: str, chapter: str) -> List[str]:
    return CURRICULUM_DATA.get(board, {}).get(grade, {}).get(subject, {}).get(chapter, [])
