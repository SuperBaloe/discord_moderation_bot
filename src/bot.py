import discord
from discord.ext import commands
import logging
import asyncio


import src.mod

###############################
#Discord connect
###############################

intents = discord.Intents.default()
intents.members = True

class ModerationBot(commands.Bot):

    def __init__(self, config):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
            chunk_guilds_at_startup=False
        )
        self.config_data = config
        self.moderation_task = None

    async def setup_hook(self):
        logging.info("Setting up Discord slash commands")
        await self.load_extension("src.commands.status_commands")
        await self.load_extension("src.commands.config_commands")
        guild = discord.Object(
            id=int(self.config_data["Guild_id"])
        )

        self.tree.copy_global_to(guild=guild)
        synced_commands = await self.tree.sync(guild=guild)

        self.moderation_task = asyncio.create_task(
            run_loop(self.config_data, self)
        )

        logging.info(
            f"Synced {len(synced_commands)} slash commands "
            f"to guild {guild.id}" 
        )

    async def on_ready(self):
        logging.info("Connected")
    

async def run_loop(config, bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            await src.mod.main(config, bot)
            wait_time = config["Check_in_time"] * 60
            logging.info(f"Waiting {config['Check_in_time']} minutes...")
            await asyncio.sleep(wait_time)


        except discord.DiscordServerError as error:
            logging.warning(f"Discord API temporarily unavailable: {error}")
            logging.info("Retrying in 60 seconds...")
            await asyncio.sleep(60)
            continue

        except discord.HTTPException as error:
            logging.error(
                f"Discord API error | Status: {error.status} | {error}"
            )
            logging.info("Retrying in 60 seconds...")
            await asyncio.sleep(60)
            continue

        except KeyError as error:
            logging.critical(
                f"Missing configuration value: {error}"
            )
            return  

        except Exception:
            logging.exception(
                "Unexpected error in moderation loop"
            )
            logging.info("Retrying in 60 seconds...")
            await asyncio.sleep(60)
            continue




def start_bot(config):
    bot = ModerationBot(config)
    bot.run(config["Token"])