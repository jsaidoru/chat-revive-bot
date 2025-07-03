import ast
from typing import Tuple


def is_safe_ast(code: str) -> Tuple[bool, str]:
    """Returns (True, '') if safe, else (False, reason)."""
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as e:
        return False, f"Syntax error: {e}"

    forbidden_nodes = {
        ast.FunctionDef: "Function definitions are not allowed.",
        ast.Lambda: "Lambdas are not allowed.",
        ast.ClassDef: "Class definitions are not allowed.",
        ast.Import: "Import statements are not allowed.",
        ast.ImportFrom: "Being clever?",
        ast.With: "`with` statements are not allowed.",
        ast.Try: "Try/except blocks are not allowed.",
        ast.Raise: "`raise` is not allowed.",
        ast.Global: "`global` is not allowed.",
        ast.Nonlocal: "`nonlocal` is not allowed.",
    }

    forbidden_names = {"eval", "exec", "__import__", "open", "compile", "input"}

    for node in ast.walk(tree):
        if type(node) in forbidden_nodes:
            return False, forbidden_nodes[type(node)]
        elif isinstance(node, ast.Call):
            # e.g., eval("...")
            if isinstance(node.func, ast.Name) and node.func.id in forbidden_names:
                return False, f"Use of `{node.func.id}()` is not allowed."
        elif isinstance(node, ast.Attribute):
            return False, "Attribute access (like `obj.attr`) is not allowed."
        elif isinstance(node, ast.Subscript):
            return False, "Subscript access (like `obj['key']`) is not allowed."

    return True, ""
