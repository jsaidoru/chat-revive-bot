from discord.ext import commands

@commands.command(name="echo")
async def echo(ctx, *, message: str):
    await ctx.message.delete()
    await ctx.send(message)