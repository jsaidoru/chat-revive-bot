import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from other_cmd import roll, help, youcanonlyusethisonceinyourlife, pingeveryone
import wolframalpha

load_dotenv()
print("DEBUG: cwd =", os.getcwd())
print("DEBUG: files =", os.listdir())

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix=">", intents=intents)
BOT_OWNER_ID = 1085862271399493732


# === BOT EVENTS ===
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore other bots
    content = message.content
    if f"<@{bot.user.id}>" in content:
        if message.author.id == 1368120467147325491:
            await message.channel.send(
                "To use Chat Revival Bot. You must consent that you do not ping jsaidoru for annoying messages."
            )
            return
        response = """Hello! I am Chat Revival Bot. My prefix is >. 
Type `>help` to see my commands.
"""
        await message.channel.send(response)
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

APP_ID = os.environ.get("APP_ID")
client = wolframalpha.Client(APP_ID)

print("APP_ID =", APP_ID)
@bot.command()
async def ask(ctx, *, query: str):
    try:
        res = await asyncio.to_thread(client.query, query)
        results = list(res.results)
        if not results:
            await ctx.send("❌ No answer found.")
            return
        answer = results[0].text
        await ctx.send(f"**Result:** {answer}")
    except Exception as e:
        await ctx.send(f"⚠️ Error: `{type(e).__name__}: {e}`")
        print("Error details:", type(e).__name__, e)
bot.remove_command("help")

bot.add_command(roll.roll)
bot.add_command(youcanonlyusethisonceinyourlife.youcanonlyusethisonceinyourlife)
bot.add_command(help.help)
bot.add_command(pingeveryone.pingeveryone)

TOKEN = os.environ.get("BOT_TOKEN")
async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

asyncio.run(main())