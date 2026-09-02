"""Main Discord music bot file."""

import os
import discord
from discord.ext import commands
from config import DISCORD_TOKEN


class MusicBot(commands.Bot):
    """Custom bot class for the music bot."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.synced = False

    async def setup_hook(self):
        """Setup hook called when bot is starting."""
        # Load all cogs
        for filename in os.listdir("cogs"):
            if filename.endswith(".py") and not filename.startswith("_"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded cog: {filename[:-3]}")

    async def on_ready(self):
        """Called when the bot is ready."""
        print(f"✅ Bot is ready! Logged in as {self.user}")

        # Sync commands with Discord (one time per session)
        if not self.synced:
            try:
                synced = await self.tree.sync()
                print(f"✅ Synced {len(synced)} command(s)")
                self.synced = True
            except Exception as e:
                print(f"❌ Failed to sync commands: {e}")


def run_bot():
    """Run the Discord bot."""
    # Set up intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    intents.guilds = True

    # Create bot instance
    bot = MusicBot(command_prefix="/", intents=intents)

    # Run the bot
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    run_bot()
