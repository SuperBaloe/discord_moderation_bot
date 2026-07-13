import discord
from discord.ext import commands
import logging
import asyncio
from datetime import datetime, timezone, time


import src.mod

###############################
#Discord connect
###############################

intents = discord.Intents.default()
intents.members = True


client = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)
Bot_config = None

class ModerationBot(commands.Bot):

    def __init__(self, config):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
            chunk_guilds_at_startup=False
        )
        self.config_data = config

    async def setup_hook(self):
        logging.info("Setting up Discord slash commands")
        await self.load_extension("src.commands.status_commands")
        await self.load_extension("src.commands.config_commands")
        guild = discord.Object(
            id=int(self.config_data["Guild_id"])
        )

        self.tree.copy_global_to(guild=guild)
        synced_commands = await self.tree.sync(guild=guild)

        logging.info(
            f"Synced {len(synced_commands)} slash commands "
            f"to guild {guild.id}" 
        )

    async def on_ready(self):
        logging.info("Connected")
        await run_loop(self.config_data, self)
    

async def run_loop(config, bot):
    while True:
        await src.mod.main(config, bot)
        wait_time = config["Check_in_time"] * 60
        logging.info(f"Waiting {config['Check_in_time']} minutes...")
        await asyncio.sleep(wait_time)


def start_bot(config):
    bot = ModerationBot(config)
    bot.run(config["Token"])