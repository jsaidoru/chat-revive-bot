import wolframalpha
from discord.ext import commands
APP_ID = "ERGYA3-7TX7YEAQ24"
client = wolframalpha.Client(APP_ID)

@commands.command()
async def ask(ctx, *, query: str):
    if not query:
        ctx.send("❌ Please include a query (e.g: integral of x^2)")
    try:
        res = client.query(query)
        answer = next(res.results).text
        await ctx.send(f"**Result:** {answer}")
    except StopIteration:
        await ctx.send("❌ No results found.")