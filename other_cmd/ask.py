import wolframalpha
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import os
load_dotenv()

APP_ID = os.environ.get("APP_ID")
client = wolframalpha.Client(APP_ID)

print("Loaded APP_ID:", APP_ID)
@commands.command()
async def ask(ctx, *, query: str):
    try:
        res = await asyncio.to_thread(client.query, query)
        results = list(res.results)
        if not results:
            await ctx.send("❌ No answer found.")
            return
        answer = results[0].text
        await ctx.send(f"**Result:** {answer}")
    except Exception as e:
        await ctx.send(f"⚠️ Error: `{type(e).__name__}: {e}`")
        print("Error details:", type(e).__name__, e)