# Bearish Discord Moderation Bot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![discord.py](https://img.shields.io/badge/discord.py-slash%20commands-5865F2)
![Version](https://img.shields.io/badge/version-0.6.5-green)
![Status](https://img.shields.io/badge/status-nightly-orange)

A lightweight Discord moderation bot that automatically checks the age of member accounts and can kick or ban accounts that are too new.

The bot supports scheduled checks, administrator-only slash commands, a whitelist, dry-run testing, configurable warning messages, action logging, and update checks.

> The `nightly` branch contains the newest features and may still contain unfinished or experimental code.

---

## Features

- Automatically checks every member in a configured Discord server
- Calculates the age of each Discord account
- Kicks or bans accounts that are younger than the configured requirement
- Runs the moderation check repeatedly at a configurable interval
- Supports a whitelist using Discord user IDs
- Ignores bot accounts
- Includes a dry-run mode for safe testing
- Can mention a flagged member before taking action
- Selects a random warning sentence from the YAML configuration
- Waits a configurable number of seconds before kicking or banning
- Reports moderation actions in a dedicated Discord channel
- Includes administrator-only slash commands
- Allows selected configuration values to be changed from Discord
- Hides the bot token when displaying the configuration
- Checks GitHub releases for newer versions
- Supports direct startup and Docker deployment
- Uses configurable logging

---

## How It Works

During every moderation cycle, the bot:

1. Loads all members from the configured Discord server.
2. Skips bot accounts.
3. Skips users on the whitelist when the whitelist is enabled.
4. Calculates the age of each Discord account.
5. Flags accounts whose age is equal to or lower than `Age_requirement`.
6. Optionally sends a warning message and mentions the member.
7. Waits for the configured `Message_time`.
8. Kicks or bans the member.
9. Reports the action in the configured bot-alarm channel.
10. Waits for `Check_in_time` minutes before checking again.

When `Dry_run` is enabled, the bot logs what it would do without kicking, banning, or sending the warning message.

---

## Requirements

- Python 3.10 or newer
- A Discord bot application
- Server Members Intent enabled
- The bot invited with the `bot` and `applications.commands` scopes

Required Python packages:

- `discord.py`
- `requests`
- `pyyaml`

Install them with:

```bash
pip install -r requirements.txt
```

---

## Discord Bot Setup

### 1. Create the bot

Create an application in the [Discord Developer Portal](https://discord.com/developers/applications), add a bot user, and copy its token.

### 2. Enable the required intent

Under **Bot → Privileged Gateway Intents**, enable:

- Server Members Intent

### 3. Invite the bot

Generate an invite URL with these scopes:

- `bot`
- `applications.commands`

Recommended bot permissions:

- View Channels
- Send Messages
- Read Message History
- Kick Members
- Ban Members

Only grant the permissions that you intend to use.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/SuperBaloe/discord_moderation_bot.git
cd discord_moderation_bot
```

To use the newest development version:

```bash
git checkout nightly
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Copy the example configuration:

### Linux or macOS

```bash
cp config/EX_config.yaml config/config.yaml
```

### Windows PowerShell

```powershell
Copy-Item config/EX_config.yaml config/config.yaml
```

Open `config/config.yaml` and enter your bot token, server ID, and channel IDs.

---

## Configuration

The runtime configuration is stored at:

```text
config/config.yaml
```

Example:

```yaml
Bot_name: bearish_bot
Token: YOUR_BOT_TOKEN

Guild_id: 123456789
Bot_alarms: 123456789

Check_in_time: 60
Age_requirement: 15

Ban_member: false
Dry_run: true

Send_sentence?: true
Channel_id: 123456789
Message_time: 10

Sentence_1: Your account is fresher than my morning coffee.
Sentence_2: You are too new for this kingdom.
Sentence_3: The age scanner beeped. Loudly.
Sentence_4: Something something Kangaroo.
Sentence_5: You must be this old to enter the ride.
Sentence_6: The bouncer checked your ID and laughed.
Sentence_7: Account still has the new-user smell.
Sentence_8: Access denied by the ancient Discord spirits.
Sentence_9: You have been bonked by the anti-spam hammer.
Sentence_10: Come back when your account has grown a beard.

Whitelist_active: true
Whitelist:
  - 329173372149825539
```

### Configuration reference

| Setting | Type | Description |
|---|---:|---|
| `Bot_name` | String | Display name used by the bot and status command |
| `Token` | String | Discord bot token |
| `Guild_id` | Integer | ID of the Discord server the bot moderates |
| `Bot_alarms` | Integer | Channel ID used for moderation reports |
| `Check_in_time` | Integer | Time between moderation checks, in minutes |
| `Age_requirement` | Integer | Accounts this age or younger are flagged |
| `Ban_member` | Boolean | `true` bans flagged members; `false` kicks them |
| `Dry_run` | Boolean | Logs actions without kicking or banning |
| `Send_sentence?` | Boolean | Sends a warning sentence before taking action |
| `Channel_id` | Integer | Channel used for warning messages |
| `Message_time` | Integer | Delay between warning and action, in seconds |
| `Sentence_1`–`Sentence_10` | String | Warning sentences selected at random |
| `Whitelist_active` | Boolean | Enables or disables whitelist checking |
| `Whitelist` | List | Discord user IDs that should never be actioned |

### Finding Discord IDs

Enable **Developer Mode** in Discord under:

```text
User Settings → Advanced → Developer Mode
```

You can then right-click a server, channel, or user and select **Copy ID**.

---

## Running the Bot

### Direct startup

The recommended startup method for the current nightly branch is:

```bash
python main_blind.py
```

The program will:

- Configure logging
- Check for an available update
- Create `config/config.yaml` when it is missing
- Load the configuration
- Connect to Discord
- Register the slash commands
- Start the recurring moderation loop

### Interactive interface

The repository also contains:

```bash
python main_interface.py
```

This interface is currently a legacy launcher. The direct `main_blind.py` startup is recommended for the current nightly branch.

---

## Slash Commands

Slash commands are synchronized to the server configured by `Guild_id`.

### Status commands

| Command | Description |
|---|---|
| `/status` | Shows whether the bot is online |
| `/ping` | Replies with `Pong!` |
| `/check_update` | Checks the latest GitHub release |

### Configuration commands

| Command | Description |
|---|---|
| `/config view` | Displays the current configuration without exposing the token |
| `/config change bot_name <new_name>` | Changes the configured bot name |
| `/config change check_in_time <new_timer>` | Changes the check interval |
| `/config change bot_alarms <new_alarm_id>` | Changes the moderation report channel |
| `/config change age_requirement <new_age>` | Changes the account-age requirement |

The configuration command group requires Discord administrator permission. Responses containing configuration data are sent ephemerally, so only the command user can see them.

Configuration changes are written directly to `config/config.yaml` and also update the configuration currently held by the running bot.

> Some settings only affect the next moderation cycle. Changes to the guild ID or bot token require a restart and are not currently exposed through slash commands.

---

## Whitelist

Enable the whitelist:

```yaml
Whitelist_active: true
```

Add Discord user IDs:

```yaml
Whitelist:
  - 111111111111111111
  - 222222222222222222
```

When enabled, matching users are skipped before the age check is applied.

---

## Kick or Ban Mode

Kick flagged accounts:

```yaml
Ban_member: false
```

Ban flagged accounts:

```yaml
Ban_member: true
```

The bot requires the matching Discord permission, and its highest role must be above the member it is trying to moderate.

---

## Warning Messages

Enable warning messages:

```yaml
Send_sentence?: true
```

The bot randomly selects one of `Sentence_1` through `Sentence_10`, sends it in `Channel_id`, mentions the member, and waits for `Message_time` seconds before acting.

Disable warning messages:

```yaml
Send_sentence?: false
```

---

## Docker

Build the image:

```bash
docker build -t discord-moderation-bot .
```

Run the container and persist the configuration directory:

```bash
docker run -d \
  --name discord-moderation-bot \
  --restart unless-stopped \
  -v "$(pwd)/config:/usr/src/app/config" \
  discord-moderation-bot
```

View the logs:

```bash
docker logs -f discord-moderation-bot
```

Stop the container:

```bash
docker stop discord-moderation-bot
```

The included Dockerfile launches:

```text
python main_blind.py
```

---

## Project Structure

```text
discord_moderation_bot/
├── config/
│   ├── EX_config.yaml
│   ├── config.yaml
│   └── logging.yaml
├── src/
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── config_commands.py
│   │   └── status_commands.py
│   ├── bot.py
│   ├── config.py
│   ├── housey_logging.py
│   ├── mod.py
│   └── update_check.py
├── .dockerignore
├── .gitignore
├── dockerfile
├── main_blind.py
├── main_interface.py
├── requirements.txt
├── version.py
└── README.md
```

### Important files

| File | Purpose |
|---|---|
| `main_blind.py` | Recommended direct launcher |
| `main_interface.py` | Legacy or experimental interactive launcher |
| `src/bot.py` | Discord bot class, command loading, and recurring loop |
| `src/mod.py` | Member loading, age checks, whitelist, and moderation actions |
| `src/config.py` | YAML creation, loading, updating, and saving |
| `src/update_check.py` | GitHub release version checker |
| `src/commands/status_commands.py` | Status, ping, and update slash commands |
| `src/commands/config_commands.py` | Administrator configuration slash commands |
| `config/logging.yaml` | Logging configuration |
| `version.py` | Application name, version, build date, and repository details |