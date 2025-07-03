import discord
from discord.ext import commands
from discord.utils import escape_markdown, escape_mentions
import asyncio
import textwrap
from is_safe_code import is_safe_ast

safe_builtins = {"print": print, "range": range, "len": len}
safe_globals = {"__builtins__": safe_builtins}


class Execute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("Execute Python codes")
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
    async def execute(self, ctx, *, code: str):
        await ctx.send("This command might be removed from the future")
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
                timeout=3,  # ⏱️ 3-second timeout
            )

            output = stdout.decode().strip()
            if not output:
                output = "✅ Code executed with no output."

        except asyncio.TimeoutError:
            output = "❌ Timeout: Your code ran too long."
        except Exception as e:
            output = f"❌ Execution error: {e}"

        clean_output = escape_markdown(escape_mentions(output[:500]))
        if any(x in clean_output for x in ["@everyone", "@here", "<@&", "<@"]):
            await ctx.send("❌ What do you think you are trying to do?.")
            return
        await ctx.send(
            f"First 500 characters of the result: \n {clean_output}",
            allowed_mentions=discord.AllowedMentions.none(),
        )


def setup(bot):
    bot.add_cog(Execute(bot))
