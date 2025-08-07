from discord.ext import commands
import os
from dotenv import load_dotenv
import requests

if os.environ.get("WOLFRAM_APP_ID") is None:
    load_dotenv()

wolfram_app_id = os.environ.get("WOLFRAM_APP_ID")

@commands.command(help="Ask WolframAlpha. It might takes 1-3 seconds to compute, especially advanced maths like integrals and derivatives.")
@commands.cooldown(rate=1, per=20, type=commands.BucketType.user)
async def ask(ctx, *, query: str):
    searching = await ctx.send("⚙️ Querying. Please wait... This might take 3-5 seconds.")
    if not wolfram_app_id:
        await ctx.send("❌ WOLFRAM_APP_ID not set.")
        return

    url = "https://api.wolframalpha.com/v2/query"
    params = {
        "input": query,
        "appid": wolfram_app_id,
        "output": "JSON"
    }

    try:
        resp = requests.get(url, params=params)
        data = resp.json()

        # Confirm 'queryresult' is present and successful
        if not data.get("queryresult", {}).get("success", False):
            await searching.edit(content=f"<@{ctx.author.id}>\n❌ WolframAlpha couldn't understand the query.")
            return

        pods = data["queryresult"].get("pods", [])
        if not pods:
            await searching.edit(content="❌ No pods returned.")
            return

        # Try to find the Result pod
        preferred_titles = [
            "result",
            "exact result",
            "decimal approximation",
            "definite integral",
            "derivative",
            "solution",
            "basic information",
            "notable facts",
            "geographic properties",
            "properties",
            "location", 
            "timeline",
            "history",
            "family",
            "education",
            "statistics",
        ]

        pod_dict = {pod.get("title", "").lower(): pod for pod in pods}
        for title in preferred_titles:
            if title in pod_dict:
                pod = pod_dict[title]
                text = pod["subpods"][0].get("plaintext", "No result text.")
                if len(text) > 1000:
                    text = text[:1000] + "..."
                return await searching.edit(content=f"<@{ctx.author.id}>\n**{pod['title']}:** {text}")
            
        # Fallback: No preferred pods exist
        for pod in pods:
            text = pod["subpods"][0].get("plaintext", "").strip()
            if text:
                if len(text) > 1000:
                    text = text[:1000] + "..."
                return await searching.edit(content=f"<@{ctx.author.id}>\n**{pod['title']}:** {text}")

        await searching.edit(content=f"<@{ctx.author.id}>\n❓ No useful information found.")

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        await ctx.send(f"⚠️ Error: `{type(e).__name__}: {e}`")