import logging
import yaml
import os

CONFIG_FILE = "config/config.yaml"

default_config = {
    "Bot_name": "bearish_bot",
    "Token": "YOUR_BOT_TOKEN",
    #Server and alarm channel for bot
    "Guild_id": 123456789,          # server id
    "Bot_alarms:": 123456789,       # Where the bot will give info when he bans or kicks
    #Interval between check and how old account should be
    "Check_in_time": 60,            # in minutes
    "Age_requirement": 15,          # how old the account has to be before being let in
    #Ban or kick
    "Ban_member": False,
    "Dry_run": False,                # Run program without kicking or banning
    #Send message before kick/ban and delta between message and kick/ban
    "Send_sentence?": True,          # if sentence will be send
    "Channel_id": 123456789,
    "Message_time": 10,              # In seconds | how long till ban when message has been send
    "Sentence_1": "Your account is fresher than my morning coffee.", # will be send the defined time before kick/Ban
    "Sentence_2": "You are too new for this kingdom.",
    "Sentence_3": "The age scanner beeped. Loudly.",
    "Sentence_4": "Something something Kangaroo.",
    "Sentence_5": "You must be this old to enter the ride.",
    "Sentence_6": "The bouncer checked your ID and laughed.",
    "Sentence_7": "Account still has the new-user smell.",
    "Sentence_8": "Access denied by the ancient Discord spirits.",
    "Sentence_9": "You have been bonked by the anti-spam hammer.",
    "Sentence_10": "Come back when your account has grown a beard.",
    #Whitelist (duh)
    "Whitelist_active": True,
    "Whitelist":[
        329173372149825539
    ]
}

def create_config_if_missing():
    if not os.path.exists(CONFIG_FILE):
        logging.info("Config file not there. Making new one")
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            yaml.safe_dump(
                default_config,
                file,
                sort_keys=False,
                default_flow_style=False
            )


def load_config():
    logging.info("Loading config")
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file) or {}

        for key, value in default_config.items():
            if key not in config:
                config[key] = value

        save_config(config)
        return config

    except (yaml.YAMLError, FileNotFoundError):
        logging.info("Config broken or missing → recreating")
        save_config(default_config)
        return default_config.copy()


def save_config(config):
    logging.info("Saving changes to config")
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        yaml.safe_dump(
            config,
            file,
            sort_keys=False,
            default_flow_style=False
        )