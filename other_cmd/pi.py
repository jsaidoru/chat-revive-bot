from tinydb import TinyDB, Query
from discord.ext import commands
import os

storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
db = TinyDB(f"{storage_location}/pi_position.json")
pos_table = db.table('position')
Digit = Query()

# If no position yet, initialize
if not pos_table.contains(Digit.key == 'pi'):
    pos_table.insert({'key': 'pi', 'value': 1})

def get_current_position():
    result = pos_table.get(Digit.key == 'pi')
    if result is not None:
        return result['value']
    else:
        # Optionally re-initialize if missing
        pos_table.insert({'key': 'pi', 'value': 1})
        return 1

def increment_position():
    pos = get_current_position()
    pos_table.update({'value': pos + 1}, Digit.key == 'pi')

def get_nth_digit(filename, n):
    with open(filename, 'r') as f:
        if f.read(2) == "3.":
            n += 2
        else:
            f.seek(0)
        f.seek(n - 1)
        return f.read(1)

@commands.command()
async def pi(ctx):
    n = get_current_position()
    digit = get_nth_digit("app/digitsofpi.txt", n)
    await ctx.send(f"Digit #{n} of π: `{digit}`")
    increment_position()