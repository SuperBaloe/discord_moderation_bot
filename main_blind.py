import mod
import yaml
import sys

CONFIG_FILE = "config.yaml"

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        return config

    except FileNotFoundError:
        print("Config file not found")
        sys.exit(1)

    except yaml.YAMLError as e:
        print(f"Config file is not valid YAML: {e}")
        sys.exit(1)

def main():
    config = load_config()
    mod.start_bot(config)

if __name__ == "__main__":
    main()