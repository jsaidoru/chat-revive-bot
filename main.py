import discord
from discord.ext import commands
import random as rand
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='>', intents=intents)
BOT_OWNER_ID = 1085862271399493732
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
        response = """Hello! I am Chat Revival Bot. My prefix is >. 
Type `>help` to see my commands.
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
        embed.description = "Use `>help <command>` for more details."

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
                    value += f"• `>{cmd.name}` (group)\n"
                else:
                    value += f"• `>{cmd.name}`\n"

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
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.command(help = "Randomly pick an option from the choices, separate each choices with a comma")
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
async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)
asyncio.run(main())