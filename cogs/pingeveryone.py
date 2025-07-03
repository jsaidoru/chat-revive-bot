from discord.ext import commands


class PingEveryone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="dont")
    async def pingeveryone(self, ctx):
        await ctx.send("what are you trying to do")


async def setup(bot):
    await bot.add_cog(PingEveryone(bot))
