from discord.ext import commands
import wikipedia
@commands.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def wiki(ctx, *, query: str):
    try:
        wikipedia.set_lang("en")  # Make sure it's in English
        try:
            summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
        except wikipedia.exceptions.PageError:
            # fallback to search and try first result
            search_results = wikipedia.search(query)
            if not search_results:
                raise wikipedia.exceptions.PageError(query)
            summary = wikipedia.summary(search_results[0], sentences=2)

        await ctx.send(f"📚 **{query.title()}**\n{summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        await ctx.send(f"❓ Be more specific. Options: {', '.join(e.options[:5])}")
    except wikipedia.exceptions.PageError:
        await ctx.send("❌ No Wikipedia page found.")
    except Exception as e:
        await ctx.send(f"⚠️ Error: `{type(e).__name__}: {e}`")

