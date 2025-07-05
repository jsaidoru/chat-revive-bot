from discord.ext import commands

@commands.command(help="dont")
async def pingeveryone(ctx):
    await ctx.send("what are you trying to do")