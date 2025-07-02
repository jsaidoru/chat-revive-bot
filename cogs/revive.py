import discord
from discord.ext import commands
import random as rand
from discord.utils import escape_markdown, escape_mentions
class Revive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def revive(self, ctx):
        await ctx.invoke(self.bot.get_command('revive withping'))
        await ctx.send("-# check out more revive commands with >help revive!")

    @revive.command(help = "Revive a chat by pinging Chat Revival Ping role.\n")
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def withping(self, ctx):
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

    @revive.command(help = "Only picks a random question instead of pinging")
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def withoutping(self, ctx):
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

    @revive.command(help = "Revive the chat with an user-defined question! Do not use inappropriate words!")
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def manual(self, ctx, *, question: str):
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