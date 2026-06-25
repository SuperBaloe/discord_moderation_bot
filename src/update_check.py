import requests
import logging
from version import APP_NAME, APP_VERSION


update_url = "https://api.github.com/repos/SuperBaloe/discord_moderation_bot/releases/latest"

def check_for_updates():
    try:
        message = requests.get(update_url, timeout=5)

        if message.status_code != 200:
            logging.info("Could not check for updates")
            return

        data = message.json()
        online_version = data["tag_name"].lstrip("v")

        if online_version != APP_VERSION:
            logging.info(f"New version available, please update to {online_version}")
        else:
            logging.info(f"program is up to data")

    except requests.RequestException:
        logging.info("update check failed, please try again later")