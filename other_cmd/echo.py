from discord.ext import commands
from discord.utils import escape_markdown, escape_mentions

@commands.command(name="echo")
async def echo(ctx, *, message: str):
    clean_message = escape_mentions(escape_markdown(message))
    if not clean_message:
        return await ctx.send("type something to echo bruh")
    if escape_mentions(message) != message:
        return await ctx.send("nah wtf are you trying to do")
    await ctx.message.delete()
    await ctx.send(clean_message)