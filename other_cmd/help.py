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

@bot.command(name="help")
async def help(ctx, *, command_name: str = None):
    embed = discord.Embed(color=discord.Color.blurple())

    if command_name is None:
        # No args → show all commands grouped by cog
        embed.title = "📘 Help Menu"
        embed.description = "Dùng `c!help <lệnh>` để có thêm chi tiết."

        cog_commands = {}

        for cmd in ctx.bot.commands:
            if cmd.hidden:
                continue
            try:
                if not await cmd.can_run(ctx):
                        continue
            except commands.CommandError:
                continue

            cog = cmd.cog_name or "Chưa phân loại"
            cog_commands.setdefault(cog, []).append(cmd)

        for cog, commands_list in cog_commands.items():
            value = ""
            for cmd in commands_list:
                if isinstance(cmd, commands.Group):
                    value += f"• `>{cmd.name}` (nhóm lệnh)\n"
                else:
                    value += f"• `>{cmd.name}`\n"

            embed.add_field(
                name=f"📂 {cog}", value=value or "Không có lệnh.", inline=False
            )
        await ctx.send(embed=embed)
    else:
        cmd = ctx.bot.get_command(command_name)
        if cmd is None:
            await ctx.send(f"❌ Không tìm thấy lệnh `{command_name}`.")
            return

        embed.title = f"❓ Help: `{cmd.qualified_name}`"
        embed.description = cmd.help or "Không có mô tả."

        if isinstance(cmd, commands.Group) and cmd.commands:
            value = ""
            for sub in cmd.commands:
                value += (
                     f"• `>{cmd.name} {sub.name}` - {sub.help or 'Không có mô tả'}\n"
                )
            embed.add_field(name="Subcommands", value=value, inline=False)

        await ctx.send(embed=embed)
