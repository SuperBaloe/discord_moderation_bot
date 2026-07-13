import asyncio
import logging
import discord
from discord import app_commands
from discord.ext import commands
import yaml

import src.config


@app_commands.default_permissions(administrator=True)
class ConfigCommands(
    commands.GroupCog,
    group_name="config",
    group_description="View and change bot config"
):
    def __init__(self, bot):
        self.bot = bot

    async def interaction_check(
        self,
        interaction: discord.Interaction
    ) -> bool:
        if interaction.user.guild_permissions.administrator:
            return True

        raise app_commands.MissingPermissions(["administrator"])

    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            logging.info("A user tried to use command without permission")
            await interaction.response.send_message(
                "You need administrator permission to use this command.",
                ephemeral=True
            )
            return

        raise error

    @app_commands.command(
    name="view",
    description="Shows the current bot configuration"
    )

    async def view(self, interaction: discord.Interaction):
        logging.info(
            "User %s (%s) used /%s",
            interaction.user,
            interaction.user.id,
            interaction.command.qualified_name
        )

        safe_config = self.bot.config_data.copy()
        safe_config.pop("Token", None)
        config_output = yaml.safe_dump(
            safe_config,
            sort_keys=False
        )
        await interaction.response.send_message(
            f"```yaml\n{config_output}```",
            ephemeral=True
        )

#########################################################
#                Change config settings                 #
#########################################################

    change = app_commands.Group(
        name="change",
        description="Change bot configuration settings"
    )

################### Bot_name ####################

    @change.command(
        name="bot_name",
        description="Change name of the bot"
    )
    async def bot_name(
        self,
        interaction: discord.Interaction,
        new_name: str
    ):
        logging.info(
            "User %s (%s) used /%s",
            interaction.user,
            interaction.user.id,
            interaction.command.qualified_name
        )
        
        new_name = new_name.strip()

        if not new_name:
            logging.info("field input was left empty when send")
            await interaction.response.send_message(
                "The bot name cannot be empty.",
                ephemeral=True
            )
            return

        old_name = src.config.update_config_value(
        self.bot.config_data,
        "Bot_name",
        new_name
        )
        logging.info(f"Bot_name was changed from {old_name} to {new_name}")
        await interaction.response.send_message(
            f"Bot name changed from `{old_name}` to `{new_name}`.",
            ephemeral=True
        )

################### Check_in_time ####################

    @change.command(
        name="check_in_time",
        description="Change timing interval of check in minutes"
    )
    async def bot_time(
        self,
        interaction: discord.Interaction,
        new_timer: int
    ):
        logging.info(
            "User %s (%s) used /%s",
            interaction.user,
            interaction.user.id,
            interaction.command.qualified_name
        )

        if not new_timer:
            logging.info("field input was left empty when send")
            await interaction.response.send_message(
                "The check in time cannot be empty.",
                ephemeral=True
            )
            return

        old_timer = src.config.update_config_value(
        self.bot.config_data,
        "Check_in_time",
        new_timer
        )
        logging.info(f"Check_in_time was changed from {old_timer}m to {new_timer}m")
        await interaction.response.send_message(
            f"Bot name changed from `{old_timer}` to `{new_timer}`.",
            ephemeral=True
        )

################### Bot_alarm channel ####################

    @change.command(
        name="bot_alarms",
        description="Change channel id bot will be sending alarms"
    )
    async def bot_alarms(
        self,
        interaction: discord.Interaction,
        new_alarm_id: int
    ):

        logging.info(
            "User %s (%s) used /%s",
            interaction.user,
            interaction.user.id,
            interaction.command.qualified_name
        )

        if not new_alarm_id:
            logging.info("field input was left empty when send")
            await interaction.response.send_message(
                "The channel id for bot alarms cannot be empty.",
                ephemeral=True
            )
            return

        old_alarm_id = src.config.update_config_value(
        self.bot.config_data,
        "Bot_alarms",
        new_alarm_id
        )
        logging.info(f"Bot_alarms was changed from {old_alarm_id} to {new_alarm_id}")
        await interaction.response.send_message(
            f"Bot name changed from `{old_alarm_id}` to `{new_alarm_id}`.",
            ephemeral=True
        )


################### Age_requirement ####################


    @change.command(
        name="age_requirement",
        description="Change age requirment of members"
    )
    async def bot_age_check(
        self,
        interaction: discord.Interaction,
        new_age: int
    ):

        logging.info(
            "User %s (%s) used /%s",
            interaction.user,
            interaction.user.id,
            interaction.command.qualified_name
        )

        if not new_age:
            logging.info("field input was left empty when send")
            await interaction.response.send_message(
                "The age requirment for new members cannot be empty.",
                ephemeral=True
            )
            return

        old_age = src.config.update_config_value(
        self.bot.config_data,
        "Age_requirement",
        new_age
        )
        logging.info(f"Age_requirement was changed from {old_age} to {new_age}")
        await interaction.response.send_message(
            f"Bot age requirment changed from `{old_age}` to `{new_age}`.",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(ConfigCommands(bot))