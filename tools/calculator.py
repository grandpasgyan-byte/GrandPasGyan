"""
Safe Math Expression Evaluation Tool
Evaluates standard mathematical expressions securely without exec().
"""

import ast
import operator
import math
from typing import Union, Optional

# Supported operators
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.Mod: operator.mod
}

# Supported math functions
SAFE_FUNCTIONS = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sqrt": math.sqrt,
    "log": math.log,
    "pi": math.pi,
    "e": math.e
}

def evaluate_expression(expr_str: str) -> Optional[Union[float, int]]:
    """Evaluates a math string expression safely using Python AST parsing."""
    try:
        node = ast.parse(expr_str.strip(), mode="eval").body
        
        def _eval(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                return SAFE_OPERATORS[type(node.op)](left, right)
            elif isinstance(node, ast.UnaryOp):
                operand = _eval(node.operand)
                return SAFE_OPERATORS[type(node.op)](operand)
            elif isinstance(node, ast.Call):
                func_name = node.func.id
                if func_name in SAFE_FUNCTIONS:
                    args = [_eval(arg) for arg in node.args]
                    return SAFE_FUNCTIONS[func_name](*args)
                raise ValueError(f"Function {func_name} not allowed.")
            elif isinstance(node, ast.Name):
                if node.id in SAFE_FUNCTIONS:
                    return SAFE_FUNCTIONS[node.id]
                raise ValueError(f"Identifier {node.id} not allowed.")
            else:
                raise TypeError(f"Unsupported expression node: {type(node)}")
                
        return _eval(node)
    except Exception:
        return None
