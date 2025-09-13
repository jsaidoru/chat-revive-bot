from discord.ext import commands
import discord
from tinydb import TinyDB, Query
import os
import random

storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
kekwdb = TinyDB(f"{storage_location}/kekwdb_dev2.json")
skulldb = TinyDB(f"{storage_location}/skulldb.json")
User = Query()

def get_random_line(filepath: str):
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
            if lines:
                return random.choice(lines).strip()
            else:
                return None
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

@commands.command(name="work", help="Work to gain KEKWs")
@commands.cooldown(rate=1, per=600, type=commands.BucketType.user)
async def work(ctx):
    author_id = ctx.author.id
    type = random.choice(["kekw", "skull"])

    if type == "kekw":
        if not kekwdb.contains(User.id == author_id):
            kekwdb.insert({'id': author_id, 'count': 20})
            embed = discord.Embed(
                description = "Here is 20 <:KEKW:1363718257835769916> for your first time working!",
                color=random.randint(0, 0xFFFFFF)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar.url
            )
            return await ctx.send(embed=embed)
        else:
            user_data = kekwdb.get(User.id == author_id)
            amount = user_data["count"] # type: ignore
            gain = random.randint(20, max(20, amount // 3))
            kekwdb.update({'count': user_data['count'] + gain}, User.id == author_id) # type: ignore

            random_message = get_random_line("work_msg.txt")

            embed = discord.Embed(
                description = f"{random_message} {gain} <:KEKW:1363718257835769916>!!",
                color=random.randint(0, 0xFFFFFF)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar.url
            )
            return await ctx.send(embed=embed)
    else:
        if not skulldb.contains(User.id == author_id):
            skulldb.insert({'id': author_id, 'count': 20})
            embed = discord.Embed(
                description = "Here is 20 💀 for your first time working!",
                color=random.randint(0, 0xFFFFFF)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar.url
            )
            return await ctx.send(embed=embed)
        else:
            user_data = skulldb.get(User.id == author_id)
            amount = user_data["count"] # type: ignore
            gain = random.randint(20, max(20, amount // 3))
            skulldb.update({'count': user_data['count'] + gain}, User.id == author_id) # type: ignore

            random_message = get_random_line("work_msg.txt")

            embed = discord.Embed(
                description = f"{random_message} {gain} 💀!!",
                color=random.randint(0, 0xFFFFFF)
            )
            embed.set_author(
                name=ctx.author.name,
                icon_url=ctx.author.avatar.url
            )
            return await ctx.send(embed=embed)