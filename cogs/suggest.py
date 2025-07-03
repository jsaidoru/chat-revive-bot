from discord.ext import commands
from discord.utils import escape_markdown, escape_mentions
BOT_OWNER_ID = 1085862271399493732
class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    @commands.cooldown(rate=1, per=60, type=commands.BucketType.user)
    async def suggest(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Suggest your ideas! Use `>help suggest` for more info")

    @suggest.command(help = "Suggest a question to be added to the question list. Don't worry about credits.\n")
    @commands.cooldown(rate=1, per=180, type=commands.BucketType.user)
    async def question(self, ctx, *, suggestion: str):
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
        owner = await self.bot.fetch_user(BOT_OWNER_ID)

        await ctx.send(
            "✅ Suggestion sent. It will be reviewed as soon as possible. Thanks for your contribution!\n")
        await owner.send(
            f"Suggestion from {ctx.author}:\n> {clean_suggestion}"
        )

    @suggest.command(help = "Suggest a new command to be added. It can be a normal or a sub-command based on the purpose.\n")
    @commands.cooldown(rate=1, per=180, type=commands.BucketType.user)
    async def command(self, ctx, *, suggestion: str):
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

        owner = await self.bot.fetch_user(1085862271399493732)

        await ctx.send(
            "✅ Suggestion sent. It will be reviewed as soon as possible.")
        await owner.send(
            f"Suggestion from {ctx.author}:\n> {clean_suggestion}"
        )

    @suggest.command(help = "Give a feedback about the bot")
    @commands.cooldown(rate=1, per=180, type=commands.BucketType.user)
    async def feedback(self, ctx, *, feedback: str):
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

        owner = await self.bot.fetch_user(1085862271399493732)

        await ctx.send(
            "✅ Feedback sent. It will be reviewed as soon as possible.")
        await owner.send(
            f"Feedback from {ctx.author}:\n> {clean_feedback}"
        )
    @suggest.command(help = "Suggest a new command to be added. It can be a normal or a sub-command based on the purpose.\n")
    @commands.cooldown(rate=1, per=180, type=commands.BucketType.user)
    async def command(self, ctx, *, suggestion: str):
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

        owner = await self.bot.fetch_user(1085862271399493732)

        await ctx.send(
            "✅ Suggestion sent. It will be reviewed as soon as possible.")
        await owner.send(
            f"Suggestion from {ctx.author}:\n> {clean_suggestion}"
        )

    @suggest.command(help = "Suggest a news ticker")
    @commands.cooldown(rate=1, per=180, type=commands.BucketType.user)
    async def funfact(self, ctx, *, funfact: str):
        clean_funfact = escape_mentions(escape_markdown(funfact))
        if not clean_funfact:
            await ctx.send("❌ Please provide a suggestion.")
            return
        if len(clean_funfact) < 15:
            await ctx.send("❌ suggestion is too short. Please provide a detailed description.")
            return
        if len(clean_funfact) > 600:
            await ctx.send("❌ suggestion is too long. Go to <#1363732122866815077> please.")
            return

        owner = await self.bot.fetch_user(1085862271399493732)

        await ctx.send(
            "✅ Feedback sent. It will be reviewed as soon as possible.")
        await owner.send(
            f"Feedback from {ctx.author}:\n> {clean_funfact}"
        )
async def setup(bot):
    await bot.add_cog(Suggest(bot))