import discord
from discord.ext import commands
import random as rand
from randomfen import random_fen
import requests
import io

class Random(commands.Cog):
    @commands.group()
    async def random(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("🎲 RNG stuff goes here! `>help random` for more info! You can also use >roll (no subcommands)")

    @random.command(help="Generate a random chess FEN.\n")
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    async def fen(self, ctx):
        fen = random_fen()
        fen_encoded = fen.replace(" ", "%20")
        url = f"https://fen2png.com/api/?fen={fen_encoded}&raw=true"

        response = requests.get(url)
        if response.status_code == 200:
            image_bytes = io.BytesIO(response.content)
            await ctx.channel.send(content=f"Here is a random FEN and the image of the chessboard: {fen}", file=discord.File(image_bytes, "chessboard.png"))

    @random.command(help="Generate a random string of 2-64 characters.\n")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def string(self, ctx, *, length: int):
        characters = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        )
        if length > 1958:
            await ctx.send("❌ String length must be 1958 characters max.")
            return
        if length <= 0:
            await ctx.send("what the fuck stop")
            return
        if length > 700:
            await ctx.send("⚠️ Please don't generate long strings")
        random_string = "".join(rand.choice(characters) for _ in range(length))
        await ctx.send(f"Here is a random string of length {length}: `{random_string}`")

    @random.command(
        help="Generate a random number from 0 to the number specified. If not, default is 100"
    )
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def integer(self, ctx, min: int = 0, max: int = 100):
        if max < 0:
            await ctx.send("❌ Maximum number must be 0 or greater.")
            return

        number = rand.randint(min, max)
        await ctx.send(f"Here is a random number from {min} to {max}: {number}")

    @random.command(help="Generate a random fun fact")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def funfact(self, ctx):
        if ctx.channel.id != 1363717602420981934:
            return await ctx.send("❌ You can't use this command here.")
        with open("funfacts.txt", "r", encoding="utf-8") as file:
            funfacts = file.readlines()

        if not funfacts:
            await ctx.send("No fun facts found.")
            return

        index = rand.randint(0, len(funfacts) - 1)  # Line number (0-based)
        chosen = funfacts[index].strip()

        embed = discord.Embed(
            title="🧠 **Here is a fun fact**",
            description=chosen,
            color=rand.randint(0, 0xFFFFFF),
            timestamp=ctx.message.created_at,
        )

        await ctx.send(f"<@{ctx.author.id}>", embed=embed)

    @random.command(help="Generate a random news ticker")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def newsticker(self, ctx):
        if ctx.channel.id != 1363717602420981934:
            return await ctx.send("❌ You can't use this command here.")
        with open("newstickers.txt", "r", encoding="utf-8") as file:
            newstickers = file.readlines()

        if not newstickers:
            await ctx.send("No news tickers found.")
            return

        index = rand.randint(0, len(newstickers) - 1)  # Line number (0-based)
        chosen = newstickers[index].strip()

        embed = discord.Embed(
            title="🧠 **Here is a news ticker**",
            description=chosen,
            color=rand.randint(0, 0xFFFFFF),
            timestamp=ctx.message.created_at,
        )

        await ctx.send(f"<@{ctx.author.id}>", embed=embed)


async def setup(bot):
    await bot.add_cog(Random(bot))
