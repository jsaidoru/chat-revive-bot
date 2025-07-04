import discord
from discord.ext import commands
from discord.utils import escape_markdown, escape_mentions
import random as rand
import os
import json
import time
from dotenv import load_dotenv
import asyncio

load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix=">", intents=intents)
BOT_OWNER_ID = 1085862271399493732
pending_suggestions = {}  # Stores user who suggested


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
    if message.content.count("|") >= 50:
        await message.channel.send("dont abuse discord bugs")
        return
    await bot.process_commands(message)  # IMPORTANT!1!!11!


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ That command doesn't exist.")
    else:
        await ctx.send(f"⚠️ An error occurred: `{str(error)}`")
# Remove default help

bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

COOLDOWN_FILE = "cooldowns.json"

# Load or initialize cooldown file
if os.path.exists(COOLDOWN_FILE):
    with open(COOLDOWN_FILE, "r") as f:
        cooldowns = json.load(f)
else:
    cooldowns = {}

def save_cooldowns():
    with open(COOLDOWN_FILE, "w") as f:
        json.dump(cooldowns, f)

@bot.command()
async def youcanonlyusethisonceinyourlife(ctx):
    user_id = str(ctx.author.id)
    now = int(time.time())
    lifetime = 2147483647

    if user_id in cooldowns and now < cooldowns[user_id]:
        remaining = cooldowns[user_id] - now
        years = remaining // 31536000
        return await ctx.send(f"⏳ Wait {years} more years :3")

    # Set cooldown
    cooldowns[user_id] = now + lifetime
    save_cooldowns()

    await ctx.send("✅ You used this command! See you in 68 years.")

@bot.command(help="Randomly pick an option from the choices, separate each choices with a comma")
@commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
async def roll(ctx, *, choices: str):
    if "ping " in choices.lower():
        await ctx.send("Please don't randomly pick who to ping. I don't want anyone to blame my bot.")
    clean_choices = escape_mentions(escape_markdown(choices))
    items = [item.strip() for item in clean_choices.split(",")]
    if not items:
        await ctx.send("No valid options provided.")
        return
    choice = rand.choice(items)
    await ctx.send(f"You rolled: **{choice}**")

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


TOKEN = os.environ.get("BOT_TOKEN")


async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)


asyncio.run(main())
