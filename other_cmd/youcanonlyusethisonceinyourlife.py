from discord.ext import commands
from tinydb import TinyDB, Query
import time
import datetime
cooldown_db = TinyDB("/storage/cooldowns.json")
User = Query()


def hhmmss(second):
    return str(datetime.timedelta(seconds=second))


@commands.command()
async def youcanonlyusethisonceinyourlife(ctx):
    user_id = str(ctx.author.id)
    now = int(time.time())
    lifetime = 2147483647  # about 68 years

    # Check if user is already in cooldown
    record = cooldown_db.get(User.user_id == user_id)
    if record and now < record["cooldown_until"]:
        remaining = record["cooldown_until"] - now
        year = remaining / 31556926
        await ctx.send(f"⏳ Wait {hhmmss(remaining)} (or {year:.9f} years) :3")
        return
    else:
        await ctx.send(f"<@{ctx.author.id}>\n🎉 Congrats, you can use this command again. Thank you for using Chat Revival Bot!")
    # Set new cooldown
    cooldown_db.upsert(
        {"user_id": user_id, "cooldown_until": now + lifetime}, User.user_id == user_id
    )

    await ctx.send("✅ You used this command! See you in 68 years.")