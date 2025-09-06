import discord
from discord.ext import commands
from tinydb import TinyDB
import os

class SkullLeaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
        self.skulldb = TinyDB(f"{self.storage_location}/skulldb.json")
    
    @commands.group(name="skulllb", aliases=["skullleaderboard"], invoke_without_command=True)
    async def skulllb(self, ctx, *, length: int = 10):
        if length > 20:
            return await ctx.send("⚠️ Max leaderboard length is 20.")
        if length <= 0:
            return await ctx.send("are you stupid")
        
        all_users = self.skulldb.all()
        if not all_users:
            await ctx.send("No skull reactions recorded yet <:iosskull:1413708504060924004>")
            return

        sorted_users = sorted(all_users, key=lambda x: x['count'], reverse=True)

        description = ""
        for i, entry in enumerate(sorted_users[:length], start=1):
            user_id = entry['id']
            count = entry['count']

            user = ctx.guild.get_member(user_id) or await ctx.client.fetch_user(user_id)
            username = user.name if user else f"Unknown User ({user_id})"

            description += f"**{i}. {username}**: {count} <:iosskull:1413708504060924004>\n"

        embed = discord.Embed(
            title="<:iosskull:1413708504060924004> Skull Leaderboard <:iosskull:1413708504060924004>",
            description=description,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

    @skulllb.command(name="mine")
    async def myskulls(self, ctx, member: discord.Member | None = None):
        member = member or ctx.author

        all_users = self.skulldb.all()
        if not all_users:
            await ctx.send("Nobody has received any skulls yet 😔")
            return

        sorted_users = sorted(all_users, key=lambda x: x['count'], reverse=True)

        user_entry = next((u for u in sorted_users if u['id'] == member.id), None)

        if not user_entry:
            await ctx.send(f"{member.display_name} has no skulls <:KEKW:1363718257835769916>")
            return

        rank = sorted_users.index(user_entry) + 1
        count = user_entry['count']

        await ctx.send(f"{member.display_name} has **{count} <:iosskull:1413708504060924004>s** and is ranked **#{rank}** on the leaderboard!")
        
    @skulllb.command(name="reset")
    async def skullreset(self, ctx):
        if ctx.author.id != 1085862271399493732:
            await ctx.send("❌ You can't reset the leaderboard.")
            return

        self.skulldb.truncate()
        await ctx.send("✅ Leaderboard reset by a chosen one!")

async def setup(bot):
    await bot.add_cog(SkullLeaderboard(bot))