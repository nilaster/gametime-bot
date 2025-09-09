# Discord Game Time Manager Bot

A Discord bot that helps manage game scheduling across different timezones for your server members.

## Features

- **Timezone Management**: Set and store individual timezone preferences for each member
- **Time Conversion**: Convert any date/time to all registered members' local timezones
- **Game Scheduling**: Set and view upcoming game times across all timezones
- **Persistent Storage**: Saves timezone preferences and game schedules to a JSON file

## Commands

### `!timezone <timezone>`
Set your personal timezone preference.

**Examples:**
- `!timezone America/New_York`
- `!timezone Europe/London`
- `!timezone UTC`

The bot supports fuzzy matching, so you can use partial timezone names like `new_york` or `london`.

### `!time <date and time>`
Convert any date/time to all registered members' local timezones.

**Examples:**
- `!time tomorrow 3pm`
- `!time December 25 8:00 AM`
- `!time next Friday 7:30 PM`

### `!game [date and time]`
Set or view the next scheduled game time.

**Examples:**
- `!game` - View the currently scheduled game
- `!game Saturday 8pm` - Set next game for Saturday at 8pm
- `!game January 15 7:00 PM` - Set game for a specific date

## Setup

### Prerequisites
- Python 3.9 or higher
- Discord bot token

### Installation

1. Clone or download this repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory:
```bash
DISCORD_TOKEN=your_discord_bot_token_here
```

4. Run the bot:
```bash
python bot.py
```

### Creating a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the bot token and add it to your `.env` file
5. Under "Privileged Gateway Intents", enable:
   - Message Content Intent
   - Server Members Intent
6. Invite the bot to your server with appropriate permissions

## Data Storage

The bot stores data in `data.json` with the following structure:
- `members_timezones`: Dictionary mapping user IDs to their timezone preferences
- `next_game`: Timestamp of the next scheduled game (null if none set)

## Dependencies

- `discord.py` - Discord API wrapper
- `python-dotenv` - Environment variable management
- `python-dateparser` - Natural language date parsing
- `zoneinfo` - Timezone handling (Python 3.9+ standard library)

## Usage Notes

- Members must set their timezone before using time-related commands
- The bot uses natural language parsing for dates, so you can use phrases like "tomorrow", "next Friday", etc.
- All times are displayed in each member's local timezone
- Game schedules persist between bot restarts