import wolframalpha
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()

APP_ID = os.environ.get("APP_ID")
client = wolframalpha.Client(APP_ID)

@commands.command()
async def ask(ctx, *, query: str):
    try:
        res = await asyncio.to_thread(client.query, query)  # Run blocking code in a thread
        answer = next(res.results).text
        await ctx.send(f"**Result:** {answer}")
    except StopIteration:
        await ctx.send("❌ No results found.")
    except Exception as e:
        print("WolframAlpha error:", e)
        await ctx.send(f"⚠️ Error: `{type(e).__name__}: {e}`")