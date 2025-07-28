from pistonapi import PistonAPI
from discord.ext import commands
from discord.utils import escape_mentions, escape_markdown
import asyncio

@commands.command(name="execute", help="Execute Python code.")
@commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
async def execute(ctx, *, code: str):
    escaped_code = escape_mentions(escape_markdown(code))
    piston = PistonAPI()

    running = await ctx.send("⚙️ Executing code. This might take 1-5 seconds...")
    # Run piston.execute in a thread to avoid blocking
    try:
        result = await asyncio.to_thread(
            piston.execute,
            language="py",
            version="3.10.0",
            code=escaped_code
        )
    except Exception as e:
        return await ctx.send(f"❌ Error during execution:\n`{str(e)}`")

    if result:
        output = result.strip() or "*No output*"
        safe_output = escape_mentions(escape_markdown(output))
        await running.edit(content=f"✅ **Code output:**\n```py\n{safe_output}\n```")
    else:
        await running.edit(content="❌ No output received.")