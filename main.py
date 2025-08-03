import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from other_cmd import execute, roll, help, youcanonlyusethisonceinyourlife, pingeveryone, ask, coolify, pi, echo
# , info

load_dotenv(dotenv_path=".env")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=">", intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=True, replied_user=False)
BOT_OWNER_ID = 1085862271399493732


# === BOT EVENTS ===
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore other bots
    content = message.content
    if "<@1389173090956742747>" in content: # chat revival bot id = 1389173090956742747
        response = """Hello! I am Chat Revival Bot. My prefix is >. 
Type `>help` to see my commands.
"""
        await message.channel.send(response)
        return
    if content.startswith(">:"):
        return
    if message.reference:
        # Get the referenced message ID
        replied_to_message_id = message.reference.message_id
        if replied_to_message_id is None:
            return  # Defensive check

        try:
            # Fetch the actual message object
            replied_to_message = await message.channel.fetch_message(replied_to_message_id)

            # Check if the command is "delete this" and the author is the same
            if message.content.strip().lower() == "delete this" and message.author.id == replied_to_message.author.id:

                await replied_to_message.delete()
                await message.delete()
        except discord.NotFound:
            pass  # Message might already be deleted
        except discord.Forbidden:
            pass  # Bot lacks permissions
        except discord.HTTPException:
            pass  # Other API failure

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

TOKEN = os.environ.get("BOT_TOKEN")
async def main():
    async with bot:
        await load()
        if TOKEN:
            await bot.start(TOKEN)

asyncio.run(main())
