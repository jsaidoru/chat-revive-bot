from discord.ext import commands
from asteval import Interpreter

MAX_LEN = 300
BOT_OWNER_ID = 1085862271399493732
class Execute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.safe_eval = Interpreter()

    @commands.command(help="Safely evaluate math/code expressions. Sent to jsaidoru for review.")
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def evaluate(self, ctx, *, code: str):

        owner = await self.bot.fetch_user(BOT_OWNER_ID)
        await owner.send(f"Code from >evaluate by {ctx.author}:\n {code}")

        try:
            result = self.safe_eval(code)

            # Check and return any asteval errors
            if self.safe_eval.error:
                err = self.safe_eval.error[0]
                self.safe_eval.error = []
                return await ctx.send(f"❌ Error: {err.get_error()}")

            self.safe_eval.symtable.clear()

            if result is None:
                await ctx.send("✅ Code executed with no result.")
            else:
                result_str = str(result)
                if len(result_str) > MAX_LEN:
                    result_str = result_str[:MAX_LEN] + "..."
                await ctx.send(f"🧮 Result: `{result_str}`")

        except Exception as e:
            await ctx.send(f"❌ Error: `{e}`")



async def setup(bot):
    await bot.add_cog(Execute(bot))