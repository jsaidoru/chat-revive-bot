from discord.ext import tasks, commands
import discord
from tinydb import TinyDB, Query
from tinydb.operations import add, subtract
import os
import random
import datetime
import pytz

class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.storage_location = "/storage" if os.environ.get("COOLIFY_RESOURCE_UUID") else "."
        self.ticket_db = TinyDB(f"{self.storage_location}/ticket_db.json")
        self.result_db = TinyDB(f"{self.storage_location}/result_db.json")
        self.kekwdb = TinyDB(f"{self.storage_location}/kekwdb_dev2.json")
        self.User = Query()
        self.kekw_emoji = "<:KEKW:1363718257835769916>"

        self.timezone = pytz.timezone("Asia/Ho_Chi_Minh")

    def cog_unload(self):
        self.lottery_task.cancel()

    @tasks.loop(minutes=1)
    async def lottery_task(self):
        now = datetime.datetime.now(self.timezone)
        if now.hour == 17 and now.minute == 0:  # 5:00 PM
            await self.run_lottery()

    def calculate_reward(self, matches: int) -> int:
        rewards = {
            6: 10000,   # jackpot
            5: 2000,
            4: 500,
            3: 100,
            2: 20,
        }
        return rewards.get(matches, 0)


    async def reward_tickets(self, result_numbers):
        winners = []
        for ticket in self.ticket_db.all():
            user_id = ticket["id"]
            user_numbers = ticket["numbers"]

            matches = len(set(result_numbers) & set(user_numbers))
            reward = self.calculate_reward(matches)

            if reward > 0:
                winners.append((user_id, matches, reward))
                # TODO: update user’s balance in your currency DB
                self.kekwdb.update(add("count", reward), self.User.id == user_id)

        # Announce
        channel = self.bot.get_channel(1363717602420981934)
        if winners:
            msg = "🎉 **Lottery Results** 🎉\n\n"
            for uid, matches, reward in winners:
                user = await self.bot.fetch_user(uid)
                msg += f"✨ {user.mention} matched **{matches}** → won **{reward} coins**!\n"
            await channel.send(msg)
        else:
            await channel.send("😔 No winners this round...")


    async def run_lottery(self):
        numbers = random.sample(range(1, 56), 6)  # 6/55 lottery
        today = str(datetime.date.today())

        # Save result
        self.result_db.insert({"date": today, "result": numbers})

        # Announce result
        channel = self.bot.get_channel(1363717602420981934)
        await channel.send(
            f"🎉 The lottery draw has been made!\n"
            f"📅 Date: {today}\n"
            f"🏆 Winning numbers: {', '.join(map(str, numbers))}"
        )

        # Clear tickets for next draw
        self.ticket_db.truncate()


    @lottery_task.before_loop
    async def before_lottery_task(self):
        await self.bot.wait_until_ready()

    @commands.group(name="lottery")
    async def lottery(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Buy and check your lottery tickets here! Winning numbers are generated daily.")
    
    @lottery.command(name="buy")
    async def buy(self, ctx):
        cost = 10
        buyer_id = ctx.author.id
        if not self.kekwdb.contains(self.User.id == buyer_id):
            return await ctx.send(f"You don't have enough {self.kekw_emoji}!")
        
        entry = self.kekwdb.get(self.User.id == buyer_id)
        if entry["count"] < cost: # type: ignore
            return await ctx.send(f"You don't have enough {self.kekw_emoji}!")
        numbers = random.sample(range(1, 56), 6)
        await ctx.send(f"You bought a ticket! Your number is {', '.join(map(str, numbers))}")
        self.kekwdb.update(subtract("count", cost), self.User.id == buyer_id)
        self.ticket_db.insert({"id": buyer_id, "numbers": numbers, "date": str(datetime.date.today())})

    @lottery.command(name="check")
    async def check(self, ctx):
        """Show all of the user's active tickets for the current draw"""
        author_id = ctx.author.id
        tickets = self.ticket_db.search(self.User.id == author_id)

        if not tickets:
            return await ctx.send("🎟️ You don't have any active tickets right now.")

        embed = discord.Embed(
            title=f"{ctx.author.name}'s Lottery Tickets 🎟️",
            color=discord.Color.green()
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)

        for i, ticket in enumerate(tickets, start=1):
            numbers = ", ".join(map(str, ticket["numbers"]))
            embed.add_field(name=f"Ticket #{i}", value=numbers, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Lottery(bot))