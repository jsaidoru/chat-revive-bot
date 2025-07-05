from discord.ext import commands
from discord.utils import escape_markdown, escape_mentions
import random as rand

@commands.command(
    help="Randomly pick an option from the choices, separate each choice with a comma"
)
@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
async def roll(ctx, *, choices: str):
    clean_choices = escape_mentions(escape_markdown(choices))
    items = [item.strip() for item in clean_choices.split(",")]
    if not items:
        await ctx.send("No valid options provided.")
        return
    choice = rand.choice(items)
    await ctx.send(f"You rolled: **{choice}**")