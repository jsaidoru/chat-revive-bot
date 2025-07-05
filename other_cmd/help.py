import discord
from discord.ext import commands

def get_all_commands(self, cmd: commands.Command, parent=""):
    cmds = []
    qualified_name = f"{parent} {cmd.name}".strip()
    if isinstance(cmd, commands.Group):
        cmds.append((qualified_name, cmd.help))
        for sub in cmd.commands:
            cmds.extend(self.get_all_commands(sub, qualified_name))
    else:
        cmds.append((qualified_name, cmd.help))
    return cmds

@commands.command(name="help")
async def custom_help(self, ctx, *, command_name: str = None):
    embed = discord.Embed(color=discord.Color.blurple())

    if command_name is None:
        # No args → show all commands grouped by cog
        embed.title = "📘 Help Menu"
        embed.description = "Use `>help <command>` for more details."

        cog_commands = {}

        for cmd in self.bot.commands:
            if cmd.hidden:
                continue
            try:
                if not await cmd.can_run(ctx):
                        continue
            except commands.CommandError:
                continue

            cog = cmd.cog_name or "Uncategorized"
            cog_commands.setdefault(cog, []).append(cmd)

        for cog, commands_list in cog_commands.items():
            value = ""
            for cmd in commands_list:
                if isinstance(cmd, commands.Group):
                    value += f"• `>{cmd.name}` (group)\n"
                else:
                    value += f"• `>{cmd.name}`\n"

            embed.add_field(
                name=f"📂 {cog}", value=value or "No commands.", inline=False
            )
        await ctx.send(embed=embed)
    else:
        cmd = self.bot.get_command(command_name)
        if cmd is None:
            await ctx.send(f"❌ Command `{command_name}` not found.")
            return

        embed.title = f"❓ Help: `{cmd.qualified_name}`"
        embed.description = cmd.help or "No description provided."

        if isinstance(cmd, commands.Group) and cmd.commands:
            value = ""
            for sub in cmd.commands:
                value += (
                     f"• `>{cmd.name} {sub.name}` - {sub.help or 'No description'}\n"
                )
            embed.add_field(name="Subcommands", value=value, inline=False)

        await ctx.send(embed=embed)