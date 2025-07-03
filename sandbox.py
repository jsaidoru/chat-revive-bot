import sys
import math

safe_builtins = {
    "abs": abs, "max": max, "min": min, "sum": sum, "range": range,
    "len": len, "print": print, "int": int, "float": float, "str": str, "bool": bool
}

safe_globals = {
    "__builtins__": safe_builtins,
    "math": math
}

code = sys.stdin.read()
context = {}

try:
    exec(code, safe_globals, context)
    if "result" in context:
        print(context["result"])
except Exception as e:
    print(f"❌ Error: {e}")
