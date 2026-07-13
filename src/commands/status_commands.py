import asyncio
import logging
import discord
from discord import app_commands
from discord.ext import commands

import src.update_check


@app_commands.default_permissions(administrator=True)
class StatusCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="status",
        description="Shows if bot is online"
    )
    async def status(self, interaction: discord.Interaction):
        bot_name = self.bot.config_data.get(
            "Bot_name",
            "Nameless bot"
        )

        await interaction.response.send_message(
            f"{bot_name} is online.",
            ephemeral=True
    )
    
    @app_commands.command(
        name="ping",
        description="Bot alive?"
    )
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Pong!",
            ephemeral=True
    )
    
    @app_commands.command(
        name="check_update",
        description="Check for updates?"
    )
    async def check_update(self, interaction: discord.Interaction):
        result = await asyncio.to_thread(
            src.update_check.check_for_updates
        )
        await interaction.response.send_message(
            result,
            ephemeral=True
    )

async def setup(bot):
    await bot.add_cog(StatusCommands(bot))