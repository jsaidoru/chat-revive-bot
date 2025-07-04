from main import bot
from tinydb import TinyDB, Query
import time
import datetime
    
# Driver program
# Use your persistent /storage folder
cooldown_db = TinyDB('/storage/cooldowns.json')
User = Query()

def hhmmss(second):
    return str(datetime.timedelta(seconds = second))
@bot.command()
async def youcanonlyusethisonceinyourlife(ctx):
    user_id = str(ctx.author.id)
    now = int(time.time())
    lifetime = 2147483647  # about 68 years

    # Check if user is already in cooldown
    record = cooldown_db.get(User.user_id == user_id)
    if record and now < record["cooldown_until"]:
        remaining = record["cooldown_until"] - now
        return await ctx.send(f"⏳ Wait {hhmmss(remaining)} more years :3")

    # Set new cooldown
    cooldown_db.upsert(
        {"user_id": user_id, "cooldown_until": now + lifetime},
        User.user_id == user_id
    )

    await ctx.send("✅ You used this command! See you in 68 years.")