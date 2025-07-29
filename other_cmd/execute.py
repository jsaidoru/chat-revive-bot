from pistonapi import PistonAPI
from discord.ext import commands
from discord.utils import escape_mentions, escape_markdown
import asyncio
from whats_that_code.election import guess_language_all_methods

@commands.command(name="execute", help="Execute codes. Supports auto-detection of language.")
@commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
async def execute(ctx, *, code: str):
    piston = PistonAPI()
    lang = guess_language_all_methods(code)
    running = await ctx.send("⚙️ Executing code. This might take 1-5 seconds... Please note that auto-detection might have errors.")
    # Run piston.execute in a thread to avoid blocking
    try:
        result = await asyncio.to_thread(
            piston.execute,
            language=lang,
            version="default",
            code=code,
            timeout=6969
        )
    except Exception as e:
        return await ctx.send(f"❌ Error during execution:\n`{str(e)}`")

    if result:
        output = result.strip() or "*No output*"
        safe_output = escape_mentions(escape_markdown(output))
        await running.edit(content=f"✅ **Code output:**\n```py\n{safe_output}\n```")
    else:
        await running.edit(content="❌ No output received.")