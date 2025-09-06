from discord.ext import commands
import discord
from tinydb import TinyDB
import os

class KekwLeaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
        self.kekwdb = TinyDB(f"{self.storage_location}/kekwdb_dev2.json")

    @commands.group(name="kekwlb", aliases=["kekwleaderboard"], invoke_without_command=True)
    async def kekwlb(self, ctx, *, length: int = 10):
        if length > 20:
            return await ctx.send("⚠️ Max leaderboard length is 20.")
        if length <= 0:
            return await ctx.send("are you stupid")
        
        all_users = self.kekwdb.all()
        if not all_users:
            await ctx.send("No KEKW reactions recorded yet 😔")
            return

        # Sort users by count (highest first)
        sorted_users = sorted(all_users, key=lambda x: x['count'], reverse=True)

        description = ""
        for i, entry in enumerate(sorted_users[:length], start=1):
            user_id = entry['id']
            count = entry['count']

            user = ctx.guild.get_member(user_id) or await ctx.cbot.fetch_user(user_id)
            username = user.name if user else f"Unknown User ({user_id})"

            description += f"**{i}. {username}**: {count} <:KEKW:1363718257835769916>\n"

        # Create embed
        embed = discord.Embed(
            title="<:KEKW:1363718257835769916> KEKW Leaderboard <:KEKW:1363718257835769916>",
            description=description,
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)
    @kekwlb.command(name="mine")
    async def mykekws(self, ctx, member: discord.Member | None = None):
        member = member or ctx.author  # default to whoever called the command

        all_users = self.kekwdb.all()
        if not all_users:
            await ctx.send("Nobody has received any KEKWs yet 😔")
            return

        sorted_users = sorted(all_users, key=lambda x: x['count'], reverse=True)

        user_entry = next((u for u in sorted_users if u['id'] == member.id), None)

        if not user_entry:
            await ctx.send(f"{member.display_name} has no KEKWs yet 😔")
            return

        rank = sorted_users.index(user_entry) + 1
        count = user_entry['count']

        await ctx.send(f"<:KEKW:1363718257835769916> {member.display_name}(you) has **{count} <:KEKW:1363718257835769916>s** and is ranked **#{rank}** on the leaderboard!")

    @kekwlb.command(name="reset")
    async def kekwreset(self, ctx):
        if ctx.author.id != 1085862271399493732:
            await ctx.send("❌ You can't reset the leaderboard.")
            return

        self.kekwdb.truncate()
        await ctx.send("✅ Leaderboard reset by a chosen one!")

async def setup(bot):
    await bot.add_cog(KekwLeaderboard(bot))