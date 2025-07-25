import discord
from discord.ext import commands
import random as rand
from tinydb import TinyDB, Query
import os

class Revive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
        self.db = TinyDB(f"{storage_location}/asked_questions_2.json")
        self.Question = Query()
        self.BOT_OWNER_ID: int = 1085862271399493732

    # Load questions from a txt file, you can specify a context if needed
    def load_questions(self, filepath='questions.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    # Get a new question, accepts a context to track different sets of questions
    def get_new_question(self, context='default'):
        # Load all questions (you could load different questions based on context)
        all_questions = self.load_questions()

        # Get previously asked questions for this context
        asked = {q['text'] for q in self.db.search(self.Question.context == context)}

        # Get remaining questions for the specific context
        remaining = [q for q in all_questions if q not in asked]

        # If no remaining questions, return a message
        if not remaining:
            return "All questions in this category have been asked!"

        # Choose a random question from remaining
        question = rand.choice(remaining)

        # Insert the new question into the database with the context
        self.db.insert({'text': question, 'context': context})

        return question

    cooldown: float = 600
    @commands.group(invoke_without_command=True)
    @commands.cooldown(rate=1, per=cooldown, type=commands.BucketType.user)
    async def revive(self, ctx):
        await ctx.invoke(self.bot.get_command("revive withping"))
        await ctx.send("-# check out more revive commands with >help revive!")

    @revive.command(help="Revive a chat by pinging Chat Revival Ping role.\n")
    @commands.cooldown(rate=1, per=cooldown, type=commands.BucketType.user)
    async def withping(self, ctx):
        if ctx.channel.id != 1363717602420981934:
            return await ctx.send("❌ You can't use this command here.")
        

        chosen = self.get_new_question(context='withping')

        embed = discord.Embed(
            title="🧠 **Revival question**",
            description=chosen,
            color=rand.randint(0, 0xFFFFFF),
            timestamp=ctx.message.created_at,
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )

        await ctx.send(
            f"""# <@&1376043512927359096>
    # <:PINGPONGSOMEONERIVIVIED:1389438166116597821><:PINGPONGSOMEONERIVIVIED:1389438166116597821><:PINGPONGSOMEONERIVIVIED:1389438166116597821>**You have been summoned for revival by {ctx.author.display_name}!!!**""",
            embed=embed,
        )
    @withping.before_invoke
    async def reset_cooldown_for_owner_withping(self, ctx):
        if ctx.author.id == self.BOT_OWNER_ID:
            ctx.command.reset_cooldown(ctx)

    @revive.command(help="Only picks a random question instead of pinging")
    @commands.cooldown(rate=1, per=cooldown, type=commands.BucketType.user)
    async def withoutping(self, ctx):
        if ctx.channel.id != 1363717602420981934:
            return await ctx.send("❌ You can't use this command here.")
        
        chosen = self.get_new_question(context='withoutping')
        embed = discord.Embed(
            title="🧠 **Random Revival Question**",
            description=chosen,
            color=rand.randint(0, 0xFFFFFF),
            timestamp=ctx.message.created_at,
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
        await ctx.send(embed=embed)
    @withoutping.before_invoke
    async def reset_cooldown_for_owner_withoutping(self, ctx):
        if ctx.author.id == self.BOT_OWNER_ID:
            ctx.command.reset_cooldown(ctx)
    
    @revive.command(help="Revive chat with manual questions.")
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def manual(self, ctx, *, question: str):
        if ctx.channel.id != 1363717602420981934:
            return await ctx.send("❌ You can't use this command here.")

        embed = discord.Embed(
            title="🧠 **Manual Revival Question**",
            description=question,
            color=rand.randint(0, 0xFFFFFF),
            timestamp=ctx.message.created_at,
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )

        await ctx.send(embed=embed)
    @manual.before_invoke
    async def reset_cooldown_for_owner_manual(self, ctx):
        if ctx.author.id == self.BOT_OWNER_ID:
            ctx.command.reset_cooldown(ctx)


async def setup(bot):
    await bot.add_cog(Revive(bot))