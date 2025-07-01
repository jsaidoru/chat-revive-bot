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
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore other bots
    
    response = """Hello! I am Chat Revival Bot. My prefix is >. Here are some commands you can use:
    revive: Ping Chat Revival Ping role to (maybe) revive a chat.
    suggestquestion: Suggest a revival question to increase randomness.
    ~~pingeveryone: Ping everyone in the server~~ nothing.
    """

    if "<@1389173090956742747>" in message.content:
        await message.channel.send(response)
    await bot.process_commands(message)

    
@bot.command
@commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
async def revive(ctx):
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
async def suggestquestion(ctx, *, suggestion: str):
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
    
    await ctx.send("✅ Suggestion sent. It will be reviewed as soon as possible.")
    await owner.send(f"📬 Yo jsaidoru, {ctx.message.author} suggested: “{suggestion}” for revival questions.")
async def pingeveryone(ctx):
    await ctx.send("what are you trying to do")

TOKEN = os.environ.get('BOT_TOKEN')
bot.run(TOKEN)