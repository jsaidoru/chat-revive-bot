import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from other_cmd import execute, roll, help, youcanonlyusethisonceinyourlife, pingeveryone, ask, coolify, pi, echo, sha256
# , info
from tinydb import TinyDB, Query

load_dotenv(dotenv_path=".env")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix=">", 
                   intents=intents, 
                   allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=True, replied_user=False))
BOT_OWNER_ID = 1085862271399493732


# === BOT EVENTS ===
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore other bots
    content = message.content
    if content.startswith(">:"):
        return
    if message.reference:
        replied_to_message_id = message.reference.message_id
        if replied_to_message_id is None:
            return

        try:
            replied_to_message = await message.channel.fetch_message(replied_to_message_id)
            if message.content.strip().lower() == "delete this" and message.author.id == replied_to_message.author.id:

                await replied_to_message.delete()
                await message.delete()
        except discord.NotFound:
            pass
        except discord.HTTPException:
            pass

    await bot.process_commands(message)  # IMPORTANT!1!!11!


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ That command doesn't exist.")
    else:
        await ctx.send(f"⚠️ An error occurred: `{str(error)}`")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
kekwdb = TinyDB(f"{storage_location}/kekwdb_dev2.json")
User = Query()
skulldb = TinyDB(f"{storage_location}/skulldb.json")
@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return

    if user.id == reaction.message.author.id:
        return
    
    if isinstance(reaction.emoji, discord.Emoji) or isinstance(reaction.emoji, discord.PartialEmoji):
        if reaction.emoji.id == 1363718257835769916: # KEKW
            if not kekwdb.contains(User.id == user.id):
                kekwdb.insert({'id': user.id, 'count': 1})
            else:
                user_data = kekwdb.get(User.id == user.id)
                if user_data is not None:
                    kekwdb.update({'count': user_data['count'] + 1}, User.id == user.id) # type: ignore
    if str(reaction.emoji) in ["💀", "☠️"]:
        receiver_id = reaction.message.author.id

        if not skulldb.contains(User.id == receiver_id):
            skulldb.insert({'id': receiver_id, 'count': 1})
        else:
            user_data = skulldb.get(User.id == receiver_id)
            if user_data is not None:
                skulldb.update({'count': user_data['count'] + 1}, User.id == receiver_id)  # type: ignore

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

bot.remove_command("help")

bot.add_command(roll.roll)
bot.add_command(youcanonlyusethisonceinyourlife.youcanonlyusethisonceinyourlife)
bot.add_command(help.help)
bot.add_command(pingeveryone.pingeveryone)
bot.add_command(ask.ask)
# bot.add_command(info.info)
bot.add_command(coolify.coolify)
bot.add_command(pi.pi)
bot.add_command(echo.echo)
bot.add_command(execute.execute)
bot.add_command(sha256.sha256_discord)

TOKEN = os.environ.get("BOT_TOKEN")
async def main():
    async with bot:
        await load()
        if TOKEN:
            await bot.start(TOKEN)

asyncio.run(main())
