from discord.ext import commands
from discord.utils import escape_mentions
import requests
import asyncio
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "pychess.py")
with open(FILE_PATH, "r", encoding="utf-8") as f:
    source = f.read()

async def run_code(code):
    def send_request():
        url = "https://emkc.org/api/v2/piston/execute"
        payload = {
            "language": "python",
            "version": "3.10.0",
            "files": [
                {"name": "main.py", "content": code},
                {"name": "chess.py", "content": source}
            ],
            "main": "main.py"
        }
        res = requests.post(url, json=payload)
        return res.json()

    result = await asyncio.to_thread(send_request)
    return result

@commands.command(name="execute", help="Execute Python codes.")
@commands.cooldown(rate=1, per=20, type=commands.BucketType.user)
async def execute(ctx, *, code: str):
    running = await ctx.send("⚙️ Executing code. This might take 1-5 seconds...")

    try:
        result = await run_code(code)
    except Exception as e:
        return await ctx.send(f"❌ Error during execution:\n`{str(e)}`")

    if result:
        output: str = result["run"]["output"]
        safe_output = escape_mentions(output)
        await running.edit(content=f"""✅ **Code output:**
```
{safe_output}
```""")
    else:
        await running.edit(content="❌ No output received.")