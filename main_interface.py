import datetime as time
import discord
import questionary
import os
import yaml


import mod
#############################
# config
#############################
CONFIG_FILE = "config.yaml"

default_config = {
    "Bot_name": "bearish_bot",
    "Token": "YOUR_BOT_TOKEN",
    "Guild_id": 123456789,          # server id
    "Webhook_url": "YOUR_WEBHOOK_URL",
    "Check_in_time": 60,            # in minutes
    "Age_requirement": 15,          # how old the account has to be before being let in
}


def create_config_if_missing():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            yaml.safe_dump(
                default_config,
                file,
                sort_keys=False,
                default_flow_style=False
            )

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file) or {}

        # Fill missing keys
        for key, value in default_config.items():
            if key not in config:
                config[key] = value

        save_config(config)
        return config

    except (yaml.YAMLError, FileNotFoundError):
        print("Config broken or missing → recreating")
        save_config(default_config)
        return default_config.copy()

def save_config(config):
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
            questionary.Choice("test mode", value=2),
            questionary.Choice("options", value=3),
            questionary.Choice("exit", value=4),
        ]
    ).ask()

def main():
    create_config_if_missing()
    config = load_config()
    print(f"running discord.py version {discord.__version__}")

    while True:
        #clear_screen()
        choice = main_menu()

        if choice == 1:
            print(f"starting {config['Bot_name']}")
            mod.start_bot(config)

        elif choice == 3:
            settings_menu(config)
            config = load_config()

        elif choice == 4 or choice is None:
            break

if __name__ == "__main__":
    main()