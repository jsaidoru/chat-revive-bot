import discord
from discord.ext import commands
from tinydb import TinyDB, Query
import os

storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
kekwdb = TinyDB(f"{storage_location}/kekwdb_dev2.json")
skulldb = TinyDB(f"{storage_location}/skulldb.json")
User = Query()

@commands.command(name="balance", aliases=["bal"])
async def balance(ctx, *, name: str | None = None):
    description = ""
    if (not name) or (name == "mine"):
        member = ctx.author
    else:
        # Try to find the member in the guild
        member = discord.utils.find(
            lambda m: m.name.lower() == name.lower()
            or (m.nick and m.nick.lower() == name.lower()),
            ctx.guild.members,
        )
        if not member:
            return await ctx.send(
                f"❌ Could not find a member with the name `{name}`. You must find the exact display name/username."
            )

    kekw_entry = kekwdb.get(User.id == member.id)
    if not kekw_entry:
        description += "0 <:KEKW:1363718257835769916>"
    else:
        count = kekw_entry["count"]  # type: ignore
        description += f"**{count}** <:KEKW:1363718257835769916>"

    skull_entry = skulldb.get(User.id == member.id)
    if not skull_entry:
        description += "0 <:iosskull:1413708504060924004>"
    else:
        count = skull_entry["count"]  # type: ignore
        description += f"**{count}** <:iosskull:1413708504060924004>"

    await ctx.send(embed=discord.Embed(
        title=f"{member}'s Balance",
        description=description,
        color=discord.Color.blue()
    ))