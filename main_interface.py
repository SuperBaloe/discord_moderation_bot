import src.housey_logging
import src.update_check
src.housey_logging.configure()

import datetime as time
import discord
import questionary
import os
import yaml
import logging

import src.mod
from version import APP_NAME, APP_VERSION


#############################
# config
#############################
CONFIG_FILE = "config/config.yaml"

default_config = {
    "Bot_name": "bearish_bot",
    "Token": "YOUR_BOT_TOKEN",
    "Guild_id": 123456789,          # server id
    "Webhook_url": "YOUR_WEBHOOK_URL",
    "Check_in_time": 60,            # in minutes
    "Age_requirement": 15,          # how old the account has to be before being let in
    "Ban_member": False,
    "Dry_run": False,                # Run program without kicking or banning
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


#############################
# functions
#############################
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


#############################
# main
#############################
def settings_menu(config):
    while True:
        clear_screen()
        keys = list(config.keys())
        keys.append("Back")
        choice = questionary.select(
            "Which setting do you want to change",
            choices=keys
        ).ask()

        if choice == "Back":
            break

        current_value = config[choice]

        if isinstance(current_value, bool):
            new_value = questionary.confirm(
                f"{choice}: {current_value}").ask()

        elif isinstance(current_value, int):
            new_value = int(questionary.text(f"{choice}: {current_value}").ask())

        elif isinstance(current_value, float):
            new_value = float(questionary.text(f"{choice}: {current_value}").ask())
            
        elif isinstance(current_value, str):
            if "path" in choice:
                new_value = questionary.path(f"{choice}: {current_value}").ask() 
            else:
                new_value = questionary.text(f"{choice}: {current_value}").ask()

        config[choice] = new_value
        save_config(config)


def main_menu():
    return questionary.select(
        "==== Main Menu ====",
        choices=[
            questionary.Choice("start bot", value=1),
        #   questionary.Choice("test mode", value=2),       #will come back for dry runs
            questionary.Choice("options", value=3),
            questionary.Choice("exit", value=4),
        ]
    ).ask()


def main():
    logging.info(f"starting: {APP_NAME} | version:{APP_VERSION}")
    logging.info("Moderation bot started in interface")
    create_config_if_missing()
    config = load_config()
    print(f"running discord.py version {discord.__version__}")

    while True:
        choice = main_menu()

        if choice == 1:
            logging.info("starting bot")
            src.mod.start_bot(config)

        elif choice == 3:
            logging.info("loading info menu")
            settings_menu(config)
            config = load_config()

        elif choice == 4 or choice is None:
            break

if __name__ == "__main__":
    src.update_check.check_for_updates()
    main()