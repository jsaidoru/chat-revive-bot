from tinydb import TinyDB, Query
import os
from discord.ext import commands

storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
db = TinyDB(f"{storage_location}/password_position.json")
rockyou_table = db.table('rockyou')
Entry = Query()

# Initialize if not exists
if not rockyou_table.contains(Entry.key == 'pos'):
    rockyou_table.insert({'key': 'pos', 'value': 0})
    
def get_nth_rockyou_password(n, filename='rockyou.txt'):
    with open(filename, 'r', encoding='latin1') as f:
        for i, line in enumerate(f):
            if i == n:
                return line.strip()
    return None  # If n is out of range

@commands.command()
async def rockyou(ctx):
    entry = rockyou_table.get(Entry.key == 'pos')
    pos = entry['value']

    password = get_nth_rockyou_password(pos)
    if password is None:
        await ctx.send("✅ End of `rockyou.txt` reached.")
        return
    
    suffix = "th" if 10 <= pos % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(pos % 10, "th")
    await ctx.send(f"🔐 {pos + 1}{suffix} leaked password: `{password}`")

    # Increment for next call
    rockyou_table.update({'value': pos + 1}, Entry.key == 'pos')
