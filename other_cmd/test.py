import requests
import json
with open("pychess.py", "r", encoding="utf-8") as f:
    source = f.read()

payload = {
    "language": "python",
    "version": "3.10.0",
    "files": [
        {"name": "main.py", "content": """
import pychess as chess
import random

board = chess.Board()

moves = list(board.legal_moves)
print(random.choice(moves))
"""},
        {"name": "pychess.py", "content": source}
    ],
    "main": "main.py"
}

try:
    res = requests.post(
        "https://emkc.org/api/v2/piston/execute",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload, ensure_ascii=True)  # ensure unicode-safe
    )
    res.raise_for_status()  # Raises exception on HTTP errors (400/500)
    print("✅ Success:")
    result = res.json()
    print(result["run"]["output"])

except requests.exceptions.HTTPError as e:
    print("❌ HTTP error occurred:")
    print(f"Status code: {res.status_code}")
    try:
        print("Response body:")
        print(res.json())  # Will show detailed Piston error if available
    except json.JSONDecodeError:
        print(res.text)  # If response is not JSON
    print("\nRaw error:")
    print(str(e))

except Exception as e:
    print("❌ Some other error occurred:")
    print(str(e))