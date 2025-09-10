from discord.ext import commands
from tinydb import TinyDB, Query
import os
import discord

storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
kekwdb = TinyDB(f"{storage_location}/kekwdb_dev2.json")
skulldb = TinyDB(f"{storage_location}/skulldb.json")
User = Query()

def load_allowed(file="../user.txt"):
    try:
        with open(file, "r") as f:
            return set(int(line.strip()) for line in f if line.strip().isdigit())
    except FileNotFoundError:
        return set()

def save_allowed(allowed_ids, file="../user.txt"):
    with open(file, "w") as f:
        for uid in allowed_ids:
            f.write(f"{uid}\n")

def remove_user_from_all(user_id: int):
    kekwdb.remove(User.id == user_id)
    skulldb.remove(User.id == user_id)

@commands.command(name="ban")
@commands.is_owner()
async def ban(ctx, id: int, *, reason: str = "No reason provided"):
    member = ctx.guild.get_member(id) or await ctx.bot.fetch_user(id)

    remove_user_from_all(id)

    allowed = load_allowed()
    if id in allowed:
        allowed.remove(id)
        save_allowed(allowed)

    await ctx.send(f"🔨 {member} has been banned from all leaderboards. Reason: {reason}")