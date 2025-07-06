import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from other_cmd import roll, help, youcanonlyusethisonceinyourlife, pingeveryone
import requests

load_dotenv(dotenv_path=".env")
print(os.environ)

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

if os.environ.get("WOLFRAM_APP_ID") is None:
    load_dotenv()

wolfram_app_id = os.environ.get("WOLFRAM_APP_ID")

@bot.command()
async def ask(ctx, *, query: str):
    if not wolfram_app_id:
        await ctx.send("❌ WOLFRAM_APP_ID not set.")
        return

    url = "https://api.wolframalpha.com/v2/query"
    params = {
        "input": query,
        "appid": wolfram_app_id,
        "output": "JSON"
    }

    try:
        resp = requests.get(url, params=params)
        data = resp.json()

        # Confirm 'queryresult' is present and successful
        if not data.get("queryresult", {}).get("success", False):
            await ctx.send("❌ WolframAlpha couldn't understand the query.")
            return

        pods = data["queryresult"].get("pods", [])
        if not pods:
            await ctx.send("❌ No pods returned.")
            return

        # Try to find the Result pod
        for pod in pods:
            if pod.get("title", "").lower() == "result":
                text = pod["subpods"][0].get("plaintext", "No result text.")
                await ctx.send(f"**Result:** {text}")
                return

        # Fallback: send first pod with plaintext
        for pod in pods:
            for subpod in pod.get("subpods", []):
                if subpod.get("plaintext"):
                    await ctx.send(f"ℹ️ {pod['title']}: {subpod['plaintext']}")
                    return

        await ctx.send("❓ No useful information found.")

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        await ctx.send(f"⚠️ Error: `{type(e).__name__}: {e}`")


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