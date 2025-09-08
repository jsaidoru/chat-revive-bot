from discord.ext import commands
from tinydb import TinyDB, Query
from tinydb.operations import add
import os
import discord

storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
kekwdb = TinyDB(f"{storage_location}/kekwdb_dev2.json")
User = Query()
skulldb = TinyDB(f"{storage_location}/skulldb.json")

@commands.command(name="add")
@commands.is_owner()
async def _add(ctx, target: str, amount: int, reward_type: str):
    # Normalize reward_type
    reward_type = reward_type.lower()
    if reward_type not in ["kekw", "skull"]:
        return await ctx.send("Type must be either `kekw` or `skull`.")

    # Try to resolve user
    member = None
    # Case 1: mention or ID
    if isinstance(target, discord.Member):
        member = target
    elif target.isdigit():
        member = ctx.guild.get_member(int(target))
    else:
        # Case 2: username (may need refinement for duplicates)
        member = discord.utils.find(lambda m: m.name == target or m.display_name == target, ctx.guild.members)

    if member is None:
        return await ctx.send("User not found!")

    receiver_id = member.id

    db = kekwdb if reward_type == "kekw" else skulldb

    if not db.contains(User.id == receiver_id):
        db.insert({"id": receiver_id, "count": amount})
    else:
        db.update(add("count", amount), User.id == receiver_id)

    emoji = "<:KEKW:1363718257835769916>" if reward_type.lower() == "kekw" else "<:iosskull:1413708504060924004>"
    await ctx.send(f"✅ Added {amount} {emoji} to <@{member.id}>.")