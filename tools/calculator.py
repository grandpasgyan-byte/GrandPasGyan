"""
Safe Math Calculator
"""

import ast
import operator
import math
from typing import Union, Optional

SAFE_OPERATORS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg, ast.Mod: operator.mod
}

SAFE_FUNCTIONS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan, "sqrt": math.sqrt,
    "log": math.log, "pi": math.pi, "e": math.e
}

def evaluate_expression(expr_str: str) -> Optional[Union[float, int]]:
    try:
        node = ast.parse(expr_str.strip(), mode="eval").body
        def _eval(n):
            if isinstance(n, (ast.Num, ast.Constant)):
                return getattr(n, 'n', getattr(n, 'value', None))
            elif isinstance(n, ast.BinOp):
                return SAFE_OPERATORS[type(n.op)](_eval(n.left), _eval(n.right))
            elif isinstance(n, ast.UnaryOp):
                return SAFE_OPERATORS[type(n.op)](_eval(n.operand))
            elif isinstance(n, ast.Call):
                return SAFE_FUNCTIONS[n.func.id](*[_eval(a) for a in n.args])
            elif isinstance(n, ast.Name):
                return SAFE_FUNCTIONS[n.id]
            raise TypeError("Invalid Node")
        return _eval(node)
    except Exception:
        return None
