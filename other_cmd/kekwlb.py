import discord
from discord.ext import commands
from tinydb import TinyDB
import os

storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
kekwdb = TinyDB(f"{storage_location}/kekwdb_dev.json")
@commands.command(name="kekwlb", aliases=["kekwleaderboard"])
async def kekwlb(ctx):
    # Get all users from DB
    all_users = kekwdb.all()
    if not all_users:
        await ctx.send("No KEKW reactions recorded yet 😔")
        return

    # Sort users by count (highest first)
    sorted_users = sorted(all_users, key=lambda x: x['count'], reverse=True)

    # Build leaderboard text
    description = ""
    for i, entry in enumerate(sorted_users[:10], start=1):  # Top 10
        user_id = entry['id']
        count = entry['count']

        user = ctx.guild.get_member(user_id) or await ctx.client.fetch_user(user_id)
        username = user.name if user else f"Unknown User ({user_id})"

        description += f"**{i}. {username}** — {count} <:KEKW:1363718257835769916>\n"

    # Create embed
    embed = discord.Embed(
        title="<:KEKW:1363718257835769916> KEKW Leaderboard <:KEKW:1363718257835769916>",
        description=description,
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)