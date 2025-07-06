from discord.ext import commands
import wikipedia
@commands.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def wiki(ctx, *, query: str):
    try:
        summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
        await ctx.send(f"📚 **{query.title()}**\n{summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        await ctx.send(f"❓ Be more specific. Options: {', '.join(e.options[:5])}")
    except wikipedia.exceptions.PageError:
        await ctx.send("❌ No Wikipedia page found.")
    except Exception as e:
        await ctx.send(f"⚠️ Error: `{type(e).__name__}: {e}`")
