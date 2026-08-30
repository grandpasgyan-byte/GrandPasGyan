"""
GrandPa's Gyan - AI Answer Verification Engine
Performs post-generation arithmetic checks on model output text.
"""

import re

def verify_math_calculation(response_text: str) -> str:
    """Checks basic arithmetic expressions for numerical accuracy."""
    matches = re.findall(r"(\d+)\s*([\+\-\*\/])\s*(\d+)\s*=\s*(\d+)", response_text)

    for m in matches:
        num1, op, num2, claimed = int(m[0]), m[1], int(m[2]), int(m[3])
        actual = None
        if op == '+': actual = num1 + num2
        elif op == '-': actual = num1 - num2
        elif op == '*': actual = num1 * num2
        elif op == '/' and num2 != 0: actual = num1 // num2

        if actual is not None and actual != claimed:
            return f"\n\n> ⚠️ **Verification Warning**: Arithmetic discrepancy detected. `{num1} {op} {num2}` equals `{actual}`, but model output stated `{claimed}`."

    return ""
