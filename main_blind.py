import src.housey_logging
src.housey_logging.configure()

import yaml
import sys
import logging

import src.mod

CONFIG_FILE = "config/config.yaml"

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            logging.info("Config loaded")
        return config

    except FileNotFoundError:
        logging.debug("Config file not found")
        sys.exit(1)

    except yaml.YAMLError as e:
        logging.debug(f"Config file is not valid YAML: {e}")
        sys.exit(1)

def main():
    logging.info("Moderation bot started blind")
    config = load_config()
    src.mod.start_bot(config)

if __name__ == "__main__":
    main()