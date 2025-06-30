import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def question(ctx):
    try:
        with open('questions.txt', 'r', encoding='utf-8') as file:
            questions = file.readlines()
            if not questions:
                await ctx.send("No questions found.")
                return
            chosen = random.choice(questions).strip()
            await ctx.send(f"Question: {chosen}")
    except FileNotFoundError:
        await ctx.send("Question file not found.")

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(TOKEN)