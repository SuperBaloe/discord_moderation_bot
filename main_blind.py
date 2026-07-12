import src.housey_logging
import src.update_check
src.housey_logging.configure()

import yaml
import sys
import logging
import src.config
import src.bot


from version import APP_NAME, APP_VERSION, BUILD_DATE

def main():
    logging.info(f"starting: {APP_NAME} | version: {APP_VERSION} | build on {BUILD_DATE}")
    logging.info("Moderation bot started blind")
    src.config.create_config_if_missing()
    config = src.config.load_config()
    src.bot.start_bot(config)

if __name__ == "__main__":
    src.update_check.check_for_updates()
    main()