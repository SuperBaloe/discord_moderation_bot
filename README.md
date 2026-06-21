# Discord Moderation Bot

A lightweight Discord moderation bot that checks account age, kicks flagged members, and reports actions through a webhook.

## What It Does

- Reads settings from `config.yaml`
- Connects to a Discord guild with `discord.py`
- Checks member account age on a schedule
- Kicks members whose accounts do not meet the age requirement
- Sends webhook notifications when a member is flagged
- Can be managed with an interactive menu or run in a simple blind mode

## Files

- `main_interface.py` - interactive launcher and config editor
- `main_blind.py` - direct startup without the menu
- `mod.py` - Discord client logic and age checks
- `config.yaml` - runtime configuration used by both launchers
- `EX_config.yaml` - example config template

## Requirements

- Python 3.10 or newer
- `discord.py`
- `requests`
- `questionary` is optional and only needed for `main_interface.py`

Install the required runtime dependencies:

```bash
pip install discord.py requests
```

Install the optional interactive menu dependency if you want to use `main_interface.py`:

```bash
pip install questionary
```

## Configuration

The bot expects a `config.yaml` file in the project root.

If you do not want to use the interactive menu, you can:

- copy `EX_config.yaml` to `config.yaml`
- edit the values in `config.yaml`
- run `main_blind.py`

Common config keys are:

- `Bot_name` - display name used in the interface
- `Token` - Discord bot token
- `Guild_id` - Discord server ID to inspect
- `Webhook_url` - webhook URL used for status messages
- `Check_in_time` - check interval in minutes
- `Age_requirement` - maximum account age in days before a member is flagged
- `Ban_member` - if true member will be banned and not kicked!

`main_interface.py` creates a default `config.yaml` if it does not already exist.


## Usage

Run the interactive menu:

```bash
python main_interface.py
```

Run the bot directly without the menu:

```bash
python main_blind.py
```

## Notes

- `questionary` is only needed for the interactive menu
- The current implementation kicks members that do not meet the age requirement

## License

Use this project for your own server moderation needs and adapt it as required.
