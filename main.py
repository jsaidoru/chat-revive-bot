import discord
from discord.ext import commands
import random as rand
import os
from dotenv import load_dotenv
from randomfen import random_fen
from discord.utils import escape_markdown, escape_mentions
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)
BOT_OWNER_ID = 1085862271399493732  # replace with your Discord user ID
pending_suggestions = {}  # Stores user who suggested

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore other bots
    if message.author.id == 1368120467147325491:
        message.channel.send("kan what do you want")

    if f"<@{bot.user.id}>" in message.content:
        response = """Hello! I am Chat Revival Bot. My prefix is >. 
Type `>help` to see my commands.
"""
        await message.channel.send(response)

    await bot.process_commands(message) # IMPORTANT!1!!11!

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if ctx.author.id == BOT_OWNER_ID:
            # Skip cooldown
            await ctx.reinvoke()
        else:
            await ctx.send(f"⏳ You're doing that too often. Try again in {round(error.retry_after)}s.")
    else:
        raise error

@commands.cooldown(rate=1, per=60, type=commands.BucketType.user)

# === Revive command ===
@bot.command(help = "Revive a chat by pinging Chat Revival Ping role, or you can just answer the question the bot provided.\n")
async def revive(ctx):
    print("debug: this is working")
    with open("questions.txt", "r", encoding="utf-8") as file:
        questions = file.readlines()

    if not questions:
        await ctx.send("No questions found.")
        return

    index = rand.randint(0, len(questions) - 1)  # Line number (0-based)
    chosen = questions[index].strip()

    embed = discord.Embed(
        title="🧠 **Revival question**",
        description=chosen,
        color=rand.randint(0, 0xFFFFFF),
        timestamp=ctx.message.created_at
    )
        
    await ctx.send(f"""# <@&1376043512927359096>
# <:PINGPONGSOMEONERIVIVIED:1389438166116597821><:PINGPONGSOMEONERIVIVIED:1389438166116597821><:PINGPONGSOMEONERIVIVIED:1389438166116597821>**You have been summoned for revival by {ctx.author.display_name}!!!**""", embed=embed)

# === Suggestion commands ===
@bot.group()
async def suggest(ctx):
     if ctx.invoked_subcommand is None:
         await ctx.send("Suggest your ideas! Use `>help suggest` for more info")

@suggest.before_invoke
@commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
async def cooldown_suggest(ctx):
    pass  # No body needed, it just applies the cooldown


@suggest.command(help = "Suggest a question to be added to the question list. Don't worry about credits.\n")
async def question(ctx, *, suggestion: str):
    clean_suggestion = escape_mentions(escape_markdown(suggestion))
    if not clean_suggestion:
        await ctx.send("❌ Please provide a suggestion.")
        return
    if len(clean_suggestion) < 10:
        await ctx.send("❌ Suggestion is too short.")
        return
    if len(clean_suggestion) > 300:
        await ctx.send("❌ Suggestion is too long.")
        return
    owner = await bot.fetch_user(BOT_OWNER_ID)

    await ctx.send(
        "✅ Suggestion sent. It will be reviewed as soon as possible. Thanks for your contribution!\n")
    await owner.send(
        f"Suggestion from {ctx.author}:\n> {clean_suggestion}"
    )

@suggest.command(help = "Suggest a new command to be added. It can be a normal or a sub-command based on the purpose.\n")
async def command(ctx, *, suggestion: str):
    clean_suggestion = escape_mentions(escape_markdown(suggestion))
    if not clean_suggestion:
        await ctx.send("❌ Please provide a suggestion.")
        return
    if len(clean_suggestion) < 20:
        await ctx.send("❌ Suggestion is too short. Please provide a detailed suggestion.")
        return
    if len(clean_suggestion) > 500:
        await ctx.send("❌ Suggestion is too long. Go to <#1363732122866815077> please.")
        return

    owner = await bot.fetch_user(1085862271399493732)

    await ctx.send(
        "✅ Suggestion sent. It will be reviewed as soon as possible.")
    await owner.send(
        f"Suggestion from {ctx.author}:\n> {clean_suggestion}"
    )

@suggest.command(help = "Give a feedback about the bot")
async def feedback(ctx, *, feedback: str):
    clean_feedback = escape_mentions(escape_markdown(feedback))
    if not clean_feedback:
        await ctx.send("❌ Please provide a feedback.")
        return
    if len(clean_feedback) < 15:
        await ctx.send("❌ Feedback is too short. Please provide a detailed description.")
        return
    if len(clean_feedback) > 600:
        await ctx.send("❌ Feedback is too long. Go to <#1363732122866815077> please.")
        return

    owner = await bot.fetch_user(1085862271399493732)

    await ctx.send(
        "✅ Feedback sent. It will be reviewed as soon as possible.")
    await owner.send(
        f"Feedback from {ctx.author}:\n> {clean_feedback}"
    )



# === Random Commands ===
@bot.group()
async def random(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("You can generate random stuff. Use `>help random` for more info.")

@random.before_invoke
@commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
async def random_cooldown(ctx):
    pass  # No body needed, it just applies the cooldown
@random.command(help = "Generate a random chess FEN. You can use the FEN to play. Good luck!\n")
async def fen(ctx):
    fen = random_fen()
    await ctx.send(f"Here is a random FEN: \n `{fen}`.")

@random.command(help = "Generate a random string of 2-64 characters.\n")
async def string(ctx, *, length: int):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if length < 2 or length > 64:
        await ctx.send("❌ Length must be between 2 and 64 characters.")
        return
    random_string = ''.join(rand.choice(characters) for _ in range(length))
    await ctx.send(f"Here is a random string of length {length}: `{random_string}`")

@bot.command()
async def roll(ctx, *, choices: str):
    # choices is a string like "apple, banana, orange"
    items = [item.strip() for item in choices.split(',')]
    if not items:
        await ctx.send("No valid options provided.")
        return
    choice = rand.choice(items)
    await ctx.send(f"You rolled: **{choice}**")
@bot.command(help = "dont")
async def pingeveryone(ctx):
    await ctx.send("what are you trying to do")

@bot.command(help = "typo?")
async def reviv(ctx):
    messages = [
        """What the fuck, reviv? What's that you just said? About making typos and forgetting the letter "e"?""",
        "Did you mean revive kiddo?",
        "Reviv or surviv? You better not to mention about that guy."
    ]
    await ctx.send(rand.choice(messages))


TOKEN = os.environ.get('BOT_TOKEN')
bot.run(TOKEN)