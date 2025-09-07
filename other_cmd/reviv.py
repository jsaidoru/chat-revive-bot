from discord.ext import commands
import random

@commands.command(help="typo?")
async def reviv(ctx):
    messages = [
        """What the fuck, reviv? What's that you just said? About making typos and forgetting the letter "e"?""",
        "Did you mean revive kiddo?",
        "Reviv or surviv? You better not to mention about that guy.",
        "I think that's a tpyo. Try again.",
        "❌ That command doesn't exist. Try again."
    ]
    await ctx.send(random.choice(messages))