import asyncio
from datetime import datetime, timezone, time
import discord
import requests
import logging


intents = discord.Intents.default()
intents.members = True


client = discord.Client(intents=intents)
Bot_config = None


def send_webhook(config, message):
    url = config["Webhook_url"]
    data = {
        "content": message
    }
    requests.post(url, json=data)
    logging.debug(f"sending *{message}* to webhook {url}")


@client.event
async def on_ready():
    logging.info("Connected")
    await run_loop(Bot_config)


async def run_loop(config):
    while True:
        await main(config)
        wait_time = config["Check_in_time"] * 60
        logging.info(f"Waiting {config['Check_in_time']} minutes...")
        await asyncio.sleep(wait_time)


def start_bot(config):
    global Bot_config
    Bot_config = config
    if Bot_config is None:
        logging.debug("Config not loaded correctly to global config in mod.py")
    client.run(config["Token"])
    

async def load_members(config, client):
    members = []
    server_id = config["Guild_id"]
    guild = client.get_guild(server_id)
    
    if guild is None:
        logging.info("Guild not found")
        return []
    
    logging.debug(f"guild id:{server_id} | guild name:{guild}")

    async for member in guild.fetch_members(limit=None):
        members.append(member)
        
    logging.info(f"Loaded {len(members)} members")
    return members


def sort_members(members):
    return sorted(
        members,
        key=lambda member: member.joined_at,
        reverse=True
    )


def calc_age(member):
    now = datetime.now(timezone.utc)
    age = now - member.created_at
    return age.days

def is_whitelisted(member, config):
    if not config["Whitelist_active"]:
        return False
    whitelist = config.get("Whitelist", [])
    return member.id in whitelist


def check_age(age_days, config):
    return age_days <= config["Age_requirement"]
        

async def main(config):
    logging.info(f"Check started: {datetime.now()}")
    members = await load_members(config, client)
    channel = client.get_channel(config['Channel_id'])

    if not members:
        return
    
    sorted_members = sort_members(members)

    for member in sorted_members:
        if member.bot:
            continue
        age_days = calc_age(member)

        if is_whitelisted(member, config):
            logging.info(f"Skipping {member.name} because of whitelist")
            continue


        if check_age(age_days, config):
            reason = f"Account younger than {config['Age_requirement']} days"

            if not config["Dry_run"]:

                if config["Ban_member"]:
                    if config['Send_sentence?']:
                        await channel.send(f"{config['Sentence_Kick/Ban']} {member.mention}")
                        await asyncio.sleep(config['Message_time'])
                        await member.ban(reason=reason)
                        action = "Banned"
                        logging.debug(f"{member.name} got banned")
                    else:
                        await member.ban(reason=reason)
                        action = "Banned"
                        logging.debug(f"{member.name} got banned")
                else:
                    if config['Send_sentence?']:
                        await channel.send(f"{config['Sentence_Kick/Ban']} {member.mention}")
                        await asyncio.sleep(config['Message_time'])
                        await member.kick(reason=reason)
                        action = "Kicked"
                        logging.debug(f"{member.name} got kicked")
                    else:
                        await member.kick(reason=reason)
                        action = "Kicked"
                        logging.debug(f"{member.name} got kicked")

                logging.info(f"{action} {member.name} | age: {age_days} days")
            else:
                logging.info(f"Dry_run: {member.name} {reason}")

            send_webhook(
                config,
                f"{action} **{member.name}** | Account age: {age_days} days | Reason: {reason}"
            )

        else:
            logging.info(f"OK {member.name} | age: {age_days} days")
