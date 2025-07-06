from discord.ext import commands
import wikipedia

@commands.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def info(ctx, *, query: str):
    wikipedia.set_lang("en")

    try:
        # First try exact match (no autosuggest)
        summary = wikipedia.summary(query, sentences=2, auto_suggest=False)
        await ctx.send(f"📚 **{query.title()}**\n{summary}")
    except wikipedia.exceptions.PageError:
        # If not found, try search fallback
        search_results = wikipedia.search(query)
        if not search_results:
            await ctx.send("❌ No Wikipedia article found.")
        else:
            summary = wikipedia.summary(search_results[0], sentences=2)
            await ctx.send(f"📚 **{search_results[0]}**\n{summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        await ctx.send(f"❓ Be more specific. Options: {', '.join(e.options[:5])}")
    except Exception as e:
        await ctx.send(f"⚠️ Error: `{type(e).__name__}: {e}`")
