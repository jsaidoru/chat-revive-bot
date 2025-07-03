from discord.ext import commands
import random as rand


class Reviv(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="typo?")
    async def reviv(self, ctx):
        messages = [
            """What the fuck, reviv? What's that you just said? About making typos and forgetting the letter \"e\"?""",
            "Did you mean revive kiddo?",
            "Reviv or surviv? You better not to mention about that guy.",
        ]
        await ctx.send(rand.choice(messages))


async def setup(bot):
    await bot.add_cog(Reviv(bot))
