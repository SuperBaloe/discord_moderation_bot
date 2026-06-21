import asyncio
from datetime import datetime, timezone
import discord
import requests


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


@client.event
async def on_ready():
    print("Connected")
    await run_loop(Bot_config)

async def run_loop(config):
    while True:
        await main(config)

        wait_time = config["Check_in_time"] * 60
        print(f"Waiting {config['Check_in_time']} minutes...")

        await asyncio.sleep(wait_time)

def start_bot(config):
    global Bot_config
    Bot_config = config
    client.run(config["Token"])
    

async def load_members(config, client):
    members = []
    server_id = config["Guild_id"]
    guild = client.get_guild(server_id)
    
    if guild is None:
        print("Guild not found")
        return []

    print(f"Guild ID: {server_id}")
    print(f"Guild: {guild}")

    async for member in guild.fetch_members(limit=None):
        members.append(member)
        
    print(f"Loaded {len(members)} members")
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


def check_age(age_days, config):
    return age_days <= config["Age_requirement"]
        

async def main(config):
    print(f"Check started: {datetime.now()}")
    members = await load_members(config, client)

    if not members:
        return
    
    sorted_members = sort_members(members)

    for member in sorted_members:
        if member.bot:
            continue
        age_days = calc_age(member)

        if check_age(age_days, config):
            reason = f"Account younger than {config['Age_requirement']} days"

            print(f"Kicking {member.name} | age: {age_days} days")

            await member.kick(reason=reason)

            send_webhook(
                config,
                f"Kicked **{member.name}** | Account age: {age_days} days | Reason: {reason}"
            )

        else:
            print(f"OK {member.name} | age: {age_days} days")
