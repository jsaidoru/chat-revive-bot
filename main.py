import discord
from discord.ext import commands
from discord.utils import escape_markdown, escape_mentions
import random as rand
import os
from dotenv import load_dotenv
import asyncio
import asyncio
import textwrap
from is_safe_code import is_safe_ast

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
        response = """Hello! I am Chat Revival Bot. My prefix is >. 
Type `>help` to see my commands.
"""
        await message.channel.send(response)
    if ">chatrevivalbot" in content.replace(" ", "").lower():
        await message.channel.send("and both is better than you")
    if "HEY" in content:
        i = rand.randint(0, 10)
        if i == 5:
            await message.channel.send("BAHAHAHA")
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


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.command(help="dont")
async def pingeveryone(ctx):
    await ctx.send("what are you trying to do")


@bot.command(help="typo?")
async def reviv(ctx):
    messages = [
        """What the fuck, reviv? What's that you just said? About making typos and forgetting the letter "e"?""",
        "Did you mean revive kiddo?",
        "Reviv or surviv? You better not to mention about that guy.",
    ]
    await ctx.send(rand.choice(messages))


@bot.command("Execute Python codes")
@commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
async def execute(ctx, *, code: str):
    await ctx.send("This command might be removed from the future")
    is_safe, reason = is_safe_ast(code)
    if not is_safe:
        return await ctx.send(f"❌ Unsafe code blocked: {reason}")
    code = textwrap.dedent(code)

    try:
        proc = await asyncio.create_subprocess_exec(
            "python",
            "sandbox.py",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await asyncio.wait_for(
            proc.communicate(code.encode()),
            timeout=3,  # ⏱️ 3-second timeout
        )

        output = stdout.decode().strip()
        if not output:
            output = "✅ Code executed with no output."

    except asyncio.TimeoutError:
        output = "❌ Timeout: Your code ran too long."
    except Exception as e:
        output = f"❌ Execution error: {e}"

    clean_output = escape_markdown(escape_mentions(output[:500]))
    if any(x in clean_output for x in ["@everyone", "@here", "<@&", "<@"]):
        await ctx.send("❌ What do you think you are trying to do?.")
        return
    await ctx.send(
        f"First 500 characters of the result: \n {clean_output}",
        allowed_mentions=discord.AllowedMentions.none(),
    )


TOKEN = os.environ.get("BOT_TOKEN")


async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)


asyncio.run(main())
