from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

code = "import random; number: int = random.randint(10, 20); print(number)"
try:
    lexer = guess_lexer(code)
    print(lexer.name)  # e.g., "Python"
except ClassNotFound:
    print("Could not determine the language.")