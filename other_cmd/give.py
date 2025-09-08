from discord.ext import commands
import discord
from tinydb.operations import add, subtract
from tinydb import TinyDB, Query
import os

class NaturalNumber(int):
    def __new__(cls, arg: str):
        value = int(arg)
        if value <= 0:
            raise commands.BadArgument("Amount must be a natural number (greater than 0).")
        return int.__new__(cls, value)

storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
User = Query()
kekwdb = TinyDB(f"{storage_location}/kekwdb_dev2.json")
User = Query()
skulldb = TinyDB(f"{storage_location}/skulldb.json")

@commands.command(name="give")
async def give(ctx, member: discord.Member, amount: NaturalNumber, reward_type: str):
    if reward_type.lower() not in ["kekw", "skull"]:
        return await ctx.send("❌ Type must be either `kekw` or `skull`.")

    db = kekwdb if reward_type.lower() == "kekw" else skulldb
    giver_id = ctx.author.id
    receiver_id = member.id

    giver_data = db.get(User.id == giver_id)
    if not giver_data or giver_data["count"] < amount: # type: ignore
        return await ctx.send("You don't have enough to give noob.")

    db.update(subtract("count", amount), User.id == giver_id)

    # Add to receiver
    if not db.contains(User.id == receiver_id):
        db.insert({"id": receiver_id, "count": amount})
    else:
        db.update(add("count", amount), User.id == receiver_id)

    emoji = "<:KEKW:1363718257835769916>" if reward_type.lower() == "kekw" else "<:iosskull:1413708504060924004>"
    await ctx.send(f"✅ <@{ctx.author.id}> gave {amount} {emoji} to <@{member.id}>")