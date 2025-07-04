import discord
from discord.ext import commands
from discord.utils import escape_markdown, escape_mentions
import asyncio
import textwrap
from is_safe_code import is_safe_ast

BOT_OWNER_ID = 1085862271399493732

safe_builtins = {"print": print, "range": range, "len": len}
safe_globals = {"__builtins__": safe_builtins}

def load_trusted_ids() -> set[int]:
    try:
        with open("trustedmembers.txt", "r") as f:
            return set(int(line.strip()) for line in f if line.strip())
    except FileNotFoundError:
        return set()
trusted_ids = load_trusted_ids()
def is_trusted(user: discord.User | discord.Member) -> bool:
    return user.id in trusted_ids

class Execute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Execute Python codes. Codes will be sent to jsaidoru for review.")
    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    async def execute(self, ctx, *, code: str):
        if not is_trusted(ctx.author):
            await ctx.send("❌ You are not trusted to use this command.")
            return
        owner = await self.bot.fetch_user(BOT_OWNER_ID)
        await owner.send(f"Code from >execute by {ctx.author}:\n {code}.")
        is_safe, reason = is_safe_ast(code)
        if not is_safe:
            return await ctx.send(f"❌ Unsafe code blocked: {reason}")
        code = textwrap.dedent(code)

        try:
            proc = await asyncio.create_subprocess_exec(
                "python",
                "sandbox.py",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await asyncio.wait_for(
                proc.communicate(code.encode()),
                timeout=3,
            )

            output = stdout.decode().strip()
            if not output:
                output = "✅ Code executed with no output."

        except asyncio.TimeoutError:
            output = "❌ Timeout: Your code ran too long (max is 3 seconds)."
        except Exception as e:
            output = f"❌ Execution error: {e}"

        clean_output = escape_markdown(escape_mentions(output[:333]))
        if any(x in clean_output for x in ["@everyone", "@here", "<@&", "<@"]):
            await ctx.send("❌ What do you think you are trying to do?.")
            return
        await ctx.send(
            f"First 333 characters of the result: \n {clean_output}",
            allowed_mentions=discord.AllowedMentions.none(),
        )


async def setup(bot):
    await bot.add_cog(Execute(bot))