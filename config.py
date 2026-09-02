"""Configuration settings for the Discord music bot."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Bot Token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set. Please check your .env file.")

# Bot Configuration
BOT_PREFIX = "/"
BOT_INTENTS = ["message_content", "guild_messages", "guilds", "voice_states"]

# Music Configuration
MUSIC_TIMEOUT = 300  # Seconds before bot leaves if idle
MAX_QUEUE_SIZE = 100
DOWNLOAD_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "default_search": "ytsearch",
    "quiet": True,
    "no_warnings": True,
}
