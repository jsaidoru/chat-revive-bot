import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore other bots

    # If replying to the bot but not pinging it — ignore
    if not "<@1389173090956742747>" in message.content:
        return
    
    if bot.user in message.mentions:
        response = (
            "Did someone mention me? If this is not about reviving chat, please shut up.\n"
            "Type `!revive` to revive chat. Press `Ctrl` for nothing."
        )
        await message.channel.send(response)

    await bot.process_commands(message)

    
@bot.group()
@commands.cooldown(rate=1, per=45, type=commands.BucketType.user)
async def revive(ctx):
    if ctx.invoked_subcommand is None:
        embed = discord.Embed(
            title="Revive Commands",
            description="""Use `!revive question` to get a random question for revival.
            Use `!revive suggest` to suggest a new question.
            Use `!revive pingeveryone` to... do nothing, relax dude.""",
            color=0x7289DA
        )
        await ctx.send(embed=embed)

@revive.command()
async def question(ctx, *, question: str):
    try:
        with open('questions.txt', 'r', encoding='utf-8') as file:
            questions = file.readlines()
            if not questions:
                await ctx.send("No questions found.")
                return
            chosen = random.choice(questions).strip()
            embed = discord.Embed(title="🧠 Revival question", description=chosen, color=0x7289DA)
            await ctx.send(f"# <@&1376043512927359096> **You have been summoned for revival by {ctx.author.name}!!!**", embed=embed)
    except FileNotFoundError:
        await ctx.send("Question file not found.")
@revive.command()
async def suggestquestion(ctx):
    suggestion = ctx.message.content[len(ctx.prefix) + len(ctx.command.name):].strip()
    if not suggestion:
        await ctx.send("❌ Please provide a suggestion.")
        return
    if len(suggestion) < 10:
        await ctx.send("❌ Suggestion is too short.")
        return
    if len(suggestion) > 300:
        await ctx.send("❌ Suggestion is too long.")
        return
    special_chars = set('!@#$%^&()_[]{}|;:\'",.<>`~')
    if any(c in special_chars for c in suggestion):
        await ctx.send("xss?")
        return
    owner = await bot.fetch_user(1085862271399493732)

    await owner.send(f"📬 Yo jsaidoru, {ctx.message.author} suggested: “{suggestion}” for revival questions.")
    await ctx.send("✅ Suggestion sent. It will be reviewed as soon as possible.")
@revive.command()
async def pingeveryone(ctx):
    await ctx.send("what are you trying to do")

for cmd in bot.commands:
    print(f"{cmd} (subcommands: {[c for c in getattr(cmd, 'commands', [])]})")
TOKEN = os.environ.get('BOT_TOKEN')
bot.run(TOKEN)