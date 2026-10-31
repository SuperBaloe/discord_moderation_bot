import asyncio
from datetime import datetime, timezone, time
import discord
import logging
import random


def Pf_check(member):
    return member.avatar is not None or member.guild_avatar is not None


def Random_message(config):

    sentences = []

    for i in range(1,11):
        sentence = config.get(f"Sentence_{i}")

        if sentence:
            sentences.append(sentence)

    if sentences:
        message = random.choice(sentences)
    else:
        message = "Default kick Message"
    return message


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
        

async def main(config, client):
    logging.info(f"Check started: {datetime.now()}")
    members = await load_members(config, client)
    channel = client.get_channel(config['Channel_id'])
    bot_channel = client.get_channel(config['Bot_alarms'])

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
                    action = "Banned"
                    logging.debug(f"Attempting {action} {member.name}")
                    if config['Send_sentence?']:
                        await channel.send(f"{Random_message(config)} {member.mention}")
                        await asyncio.sleep(config['Message_time'])
                        await member.ban(reason=reason)
                    else:
                        await member.ban(reason=reason)
                    await bot_channel.send(f"{action} **{member.name}** | Account age: {age_days} days | Reason: {reason}")
                else:
                    action = "Kicked"
                    logging.debug(f"Attempting {action} {member.name}")
                    if config['Send_sentence?']:
                        await channel.send(f"{Random_message(config)} {member.mention}")
                        await asyncio.sleep(config['Message_time'])
                        await member.kick(reason=reason)
                    else:
                        await member.kick(reason=reason)
                    await bot_channel.send(f"{action} **{member.name}** | Account age: {age_days} days | Reason: {reason}")

                logging.info(f"{action} {member.name} | age: {age_days} days")
            else:
                logging.info(f"Dry_run: {member.name} {reason}")

        else:
            logging.info(f"{'OK':<6} {member.name:<32} | age: {age_days:>5} days")          #Discord max username lenght is 32