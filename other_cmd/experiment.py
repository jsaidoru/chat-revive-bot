import discord
from discord.ext import commands
from discord.ui import Button, View

@commands.command()
async def experiment(ctx):
    # Create a button
    button = Button(label="Click me!", style=discord.ButtonStyle.primary)

    # What happens when button is clicked
    async def button_callback(interaction):
        await interaction.response.send_message("You clicked the button!", ephemeral=True)

    button.callback = button_callback

    # Add button to view and send it
    view = View()
    view.add_item(button)
    await ctx.send("Here is a button:", view=view)