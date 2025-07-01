import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
from randomfen import random_fen
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
    if message.author.id == BOT_OWNER_ID and isinstance(message.channel, discord.DMChannel):
        if message.content.strip().lower() == "allowed":
            # Find the suggestion
            data = pending_suggestions.get(BOT_OWNER_ID)
            if not data:
                await message.channel.send("No suggestion to allow.")
                return

            guild = bot.get_guild(data["guild_id"])
            channel = guild.get_channel(data["channel_id"])
            member = guild.get_member(data["author_id"])
            suggestion = data["suggestion"]

            if channel and member:
                await channel.send(f"✅ Suggestion approved from {member.mention}:\n> {suggestion}")
            else:
                await message.channel.send("Could not find user or channel.")

            del pending_suggestions[BOT_OWNER_ID]
    if message.author.bot:
        return  # Ignore other bots
    if message.author.id == 1368120467147325491:
        return # kan needs to shut up
    response = """Hello! I am Chat Revival Bot. My prefix is >. Here are some commands you can use:
    revive: Ping Chat Revival Ping role to (maybe) revive a chat.
    suggestquestion: Suggest a revival question to increase randomness.
    ~~pingeveryone: Ping everyone in the server~~ nothing.
    """

    if "<@1389173090956742747>" in message.content:
        await message.channel.send(response)

    await bot.process_commands(message)


@bot.command()
@commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
async def revive(ctx):
    with open("questions.txt", "r", encoding="utf-8") as file:
        questions = file.readlines()

    if not questions:
        await ctx.send("No questions found.")
        return

    index = random.randint(0, len(questions) - 1)  # Line number (0-based)
    chosen = questions[index].strip()

    embed = discord.Embed(
        title="🧠 **Revival question**",
        description=chosen,
        color=random.randint(0, 0xFFFFFF),
        timestamp=ctx.message.created_at
    )
        
    await ctx.send(f"# <@&1376043512927359096> \n <:PINGPONGSOMEONERIVIVIED:1389438166116597821><:PINGPONGSOMEONERIVIVIED:1389438166116597821><:PINGPONGSOMEONERIVIVIED:1389438166116597821>**You have been summoned for revival by {ctx.author.display_name}!!!**", embed=embed)


@bot.command()
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
    special_chars = set(r'@#$%^&()_|;:\,.<>`~')
    if any(c in special_chars for c in suggestion):
        await ctx.send("xss?")
        return

    owner = await bot.fetch_user(BOT_OWNER_ID)

    await ctx.send(
        "✅ Suggestion sent. It will be reviewed as soon as possible. Thanks for your contribution!")
    await owner.send(
        f"Suggestion from {ctx.author}:\n> {suggestion}\nReply with 'allowed' to approve it."
    )
    pending_suggestions[owner.id] = {
        "author_id": ctx.author.id,
        "guild_id": ctx.guild.id,
        "channel_id": ctx.channel.id,
        "suggestion": suggestion
    }
@bot.command()
async def suggestcommand(ctx, *, suggestion: str):
    if not suggestion:
        await ctx.send("❌ Please provide a suggestion.")
        return
    if len(suggestion) < 20:
        await ctx.send("❌ Suggestion is too short. Please provide a detailed suggestion.")
        return
    if len(suggestion) > 500:
        await ctx.send("❌ Suggestion is too long. Go to <#1363732122866815077> please.")
        return
    special_chars = set(r'@#$%^&()_|;:\,.<>`~')
    if any(c in special_chars for c in suggestion):
        await ctx.send("what do you think you are doing?")
        return

    owner = await bot.fetch_user(1085862271399493732)

    await ctx.send(
        "✅ Suggestion sent. It will be reviewed as soon as possible.")
    await owner.send(
        f"📬 Yo jsaidoru, {ctx.message.author} suggested: “{suggestion}” for revival questions."
    )

@bot.command()
async def randomfen(ctx):
    fen = random_fen()
    await ctx.send(f"Here is a random FEN: \n `{fen}`. Good luck playing with that position!")
@bot.command()
async def pingeveryone(ctx):
    await ctx.send("what are you trying to do")

TOKEN = os.environ.get('BOT_TOKEN')
bot.run(TOKEN)