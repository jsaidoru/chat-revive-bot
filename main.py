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

# === BOT EVENTS ===
@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore other bots
    if message.author.id == 1368120467147325491:
        # message.channel.send("kan what do you want")
        return
    content = message.content
    if f"<@{bot.user.id}>" in content:
        response = """Hello! I am Chat Revival Bot. My prefix is >(will be changed in the future). 
Type `,help` to see my commands.
"""
        await message.channel.send(response)
    if ">chatrevivalbot" in content.replace(" ", "").lower():
        await message.channel.send("and both is better than you")
    if "HEY" in content:
        i = rand.randint(0, 10)
        if i == 5: await message.channel.send("BAHAHAHA")
    await bot.process_commands(message) # IMPORTANT!1!!11!

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ That command doesn't exist.")
    else:
        await ctx.send(f"⚠️ An error occurred: `{str(error)}`")

# Remove default help

bot.remove_command('help')

# Recursive function to get command and its subcommands
def get_all_commands(cmd: commands.Command, parent=""):
    cmds = []
    qualified_name = f"{parent} {cmd.name}".strip()
    if isinstance(cmd, commands.Group):
        cmds.append((qualified_name, cmd.help))
        for sub in cmd.commands:
            cmds.extend(get_all_commands(sub, qualified_name))
    else:
        cmds.append((qualified_name, cmd.help))
    return cmds

@bot.command(name="help")
async def custom_help(ctx, *, command_name: str = None):
    embed = discord.Embed(
        color=discord.Color.blurple()
    )

    if command_name is None:
        # No args → show all commands grouped by cog
        embed.title = "📘 Help Menu"
        embed.description = "Use `!help <command>` for more details."

        cog_commands = {}

        for cmd in bot.commands:
            if cmd.hidden:
                continue
            try:
                if not await cmd.can_run(ctx):
                    continue
            except commands.CommandError:
                continue

            cog = cmd.cog_name or "Uncategorized"
            cog_commands.setdefault(cog, []).append(cmd)

        for cog, commands_list in cog_commands.items():
            value = ""
            for cmd in commands_list:
                if isinstance(cmd, commands.Group):
                    value += f"• `!{cmd.name}` (group)\n"
                else:
                    value += f"• `!{cmd.name}`\n"

            embed.add_field(name=f"📂 {cog}", value=value or "No commands.", inline=False)
        await ctx.send(embed=embed)
    else:
        # User typed: >help revive, >help random
        cmd = bot.get_command(command_name)
        if cmd is None:
            await ctx.send(f"❌ Command `{command_name}` not found.")
            return

        embed.title = f"❓ Help: `{cmd.qualified_name}`"
        embed.description = cmd.help or "No description provided."

        if isinstance(cmd, commands.Group) and cmd.commands:
            value = ""
            for sub in cmd.commands:
                value += f"• `!{cmd.name} {sub.name}` - {sub.help or 'No description'}\n"
            embed.add_field(name="Subcommands", value=value, inline=False)

        await ctx.send(embed=embed)



# === Revive commands ===
@bot.group(invoke_without_command= True)
@commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
async def revive(ctx):
    await ctx.invoke(bot.get_command('revive withping'))
    await ctx.send("-# check out more revive commands with ,help revive!")

@revive.command(help = "Revive a chat by pinging Chat Revival Ping role.\n")
@commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
async def withping(ctx):
    if ctx.channel.id != 1363717602420981934:
        return await ctx.send("❌ You can't use this command here.")
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

@revive.command()
@commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
async def withoutping(ctx):
    if ctx.channel.id != 1363717602420981934:
        return await ctx.send("❌ You can't use this command here.")
    with open("questions.txt", "r", encoding="utf-8") as file:
        questions = file.readlines()

    if not questions:
        await ctx.send("No questions found.")
        return

    index = rand.randint(0, len(questions) - 1)  # Line number (0-based)
    chosen = questions[index].strip()

        
    await ctx.send(f"## Here is a random question:\n **{chosen}**")

@revive.command()
@commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
async def manual(ctx, *, question: str):
    if ctx.channel.id != 1363717602420981934:
        return await ctx.send("❌ You can't use this command here.")
    clean_question = escape_mentions(escape_markdown(question))
    embed = discord.Embed(
        title="🧠 **Revival question**",
        description=clean_question,
        color=rand.randint(0, 0xFFFFFF),
        timestamp=ctx.message.created_at
    )
        
    await ctx.send(f"""# <@&1376043512927359096>
# <:PINGPONGSOMEONERIVIVIED:1389438166116597821><:PINGPONGSOMEONERIVIVIED:1389438166116597821><:PINGPONGSOMEONERIVIVIED:1389438166116597821>**You have been summoned for revival by {ctx.author.display_name}!!!**""", embed=embed)

@revive.command()
async def withping(ctx):
    if ctx.channel.id != 1363717602420981934:
        return await ctx.send("❌ You can't use this command here.")
    with open("funfacts.txt", "r", encoding="utf-8") as file:
        funfacts = file.readlines()

    if not funfacts:
        await ctx.send("No fun facts found.")
        return

    index = rand.randint(0, len(funfacts) - 1)  # Line number (0-based)
    chosen = funfacts[index].strip()

    embed = discord.Embed(
        title="🧠 **Here is a fun fact**",
        description=chosen,
        color=rand.randint(0, 0xFFFFFF),
        timestamp=ctx.message.created_at
    )
        
    await ctx.send(f"""# <@&1376043512927359096>
# <:PINGPONGSOMEONERIVIVIED:1389438166116597821><:PINGPONGSOMEONERIVIVIED:1389438166116597821><:PINGPONGSOMEONERIVIVIED:1389438166116597821>**You have been summoned for revival by {ctx.author.display_name}!!!**""", embed=embed)
# === Suggestion commands ===
@bot.group()
@commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
async def suggest(ctx):
     if ctx.invoked_subcommand is None:
         await ctx.send("Suggest your ideas! Use `,help suggest` for more info")


@suggest.command(help = "Suggest a question to be added to the question list. Don't worry about credits.\n")
@commands.cooldown(rate=1, per=180, type=commands.BucketType.user)
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
@commands.cooldown(rate=1, per=180, type=commands.BucketType.user)
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
@commands.cooldown(rate=1, per=180, type=commands.BucketType.user)
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
        await ctx.send("You can generate random stuff. Use `,help random` for more info.")

@random.command(help = "Generate a random chess FEN.\n")
@commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
async def fen(ctx):
    fen = random_fen()
    await ctx.send(f"Here is a random FEN: \n `{fen}`.")

@random.command(help = "Generate a random string of 2-64 characters.\n")
@commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
async def string(ctx, *, length: int):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if length < 2 or length > 64:
        await ctx.send("❌ Length must be between 2 and 64 characters.")
        return
    random_string = ''.join(rand.choice(characters) for _ in range(length))
    await ctx.send(f"Here is a random string of length {length}: `{random_string}`")

@random.command(help = "Generate a random number from 0 to the number specified. If not, default is 69")
@commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
async def integer(ctx, min: int = 0, max: int = 69):
    if max < 0:
        await ctx.send("❌ Maximum number must be 0 or greater.")
        return

    number = rand.randint(min, max)
    await ctx.send(f"Here is a random number from {min} to {max}: {number}")

@bot.command()
@commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
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