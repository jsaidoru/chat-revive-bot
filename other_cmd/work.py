from discord.ext import commands
import discord
from tinydb import TinyDB, Query
import os
import random

storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
kekwdb = TinyDB(f"{storage_location}/kekwdb_dev2.json")
User = Query()

@commands.command(name="work", help="Work to gain KEKWs")
async def work(ctx):
    author_id = ctx.author.id
    if not kekwdb.contains(User.id == author_id):
        kekwdb.insert({'id': author_id, 'count': 20})
        embed = discord.Embed(
            description = "Here is 20 <:KEKW:1363718257835769916> for your first time working!"
        )
        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar.url
        )
        embed.set_footer(
            text="Working messages will come soon!"
        )
        return await ctx.send(embed=embed)
    else:
        user_data = kekwdb.get(User.id == author_id)
        amount = user_data["count"] # type: ignore
        gain = random.randint(10, max(10, amount // 3))
        kekwdb.update({'count': user_data['count'] + gain}, User.id == author_id) # type: ignore

        embed = discord.Embed(
            description = f"You gained {gain} from working!!"
        )
        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar.url
        )
        embed.set_footer(
            text="Working messages will come soon!"
        )
        return await ctx.send(embed=embed)