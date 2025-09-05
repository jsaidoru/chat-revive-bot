import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from other_cmd import execute, roll, help, youcanonlyusethisonceinyourlife, pingeveryone, ask, coolify, pi, echo, sha256, kekwlb
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
@bot.event
async def on_reaction_add(reaction, user):
    # Ignore bot's own reactions
    if user.id == bot.user.id:
        return

    # Ignore if reactor is the same as the message author (no self-KEKW farming)
    if user.id == reaction.message.author.id:
        return

    # Only count KEKW emoji
    if isinstance(reaction.emoji, (discord.Emoji, discord.PartialEmoji)) and reaction.emoji.id == 1363718257835769916:
        receiver_id = reaction.message.author.id  # << the person who RECEIVES the KEKW
        if receiver_id == 1389173090956742747: return

        user_data = kekwdb.get(User.id == receiver_id)
        if user_data is None:
            kekwdb.insert({'id': receiver_id, 'count': 1})
        else:
            count = user_data.get('count', 0)
            kekwdb.update({'count': count + 1}, User.id == receiver_id) # type: ignore

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
bot.add_command(kekwlb.kekwlb)

TOKEN = os.environ.get("BOT_TOKEN")
async def main():
    async with bot:
        await load()
        if TOKEN:
            await bot.start(TOKEN)

asyncio.run(main())
