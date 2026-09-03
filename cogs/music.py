"""Music cog for Discord music bot with slash commands."""

import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp
from config import DOWNLOAD_OPTIONS, MAX_QUEUE_SIZE
from utils.queue import MusicQueue


class Music(commands.Cog):
    """Music player commands."""

    def __init__(self, bot):
        self.bot = bot
        self.music_queues = {}  # guild_id -> MusicQueue
        self.now_playing = {}  # guild_id -> (title, url)
        self.ydl = yt_dlp.YoutubeDL(DOWNLOAD_OPTIONS)

    def get_queue(self, guild_id):
        """Get or create a music queue for a guild."""
        if guild_id not in self.music_queues:
            self.music_queues[guild_id] = MusicQueue(max_size=MAX_QUEUE_SIZE)
        return self.music_queues[guild_id]

    async def play_next(self, interaction: discord.Interaction):
        """Play the next song in the queue."""
        guild_id = interaction.guild_id
        queue = self.get_queue(guild_id)

        if queue.is_empty():
            self.now_playing[guild_id] = None
            if interaction.response.is_done():
                await interaction.followup.send("Queue is empty. Leaving voice channel.")
            return

        try:
            song = queue.get_next()
            audio_url = song["url"]
            title = song["title"]

            # Create audio source
            audio_source = discord.FFmpegPCMAudio(
                audio_url,
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                options="-vn",
            )

            voice_client = interaction.guild.voice_client

            # Play audio with async-safe callback
            def after_playing(error):
                if error:
                    print(f"Player error: {error}")
                # Schedule play_next to run in the event loop
                # Using asyncio.ensure_future for better Python 3.14 compatibility
                asyncio.run_coroutine_threadsafe(
                    self.play_next(interaction), self.bot.loop
                )

            voice_client.play(audio_source, after=after_playing)

            # Update now_playing
            self.now_playing[guild_id] = (title, song["webpage_url"])

            if interaction.response.is_done():
                await interaction.followup.send(
                    f"🎵 Now playing: **{title}**\n{song['webpage_url']}"
                )
            else:
                await interaction.response.send_message(
                    f"🎵 Now playing: **{title}**\n{song['webpage_url']}"
                )

        except Exception as e:
            print(f"Error playing audio: {e}")
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error playing audio: {str(e)}"
                )

    def extract_video_info(self, url):
        """Extract video information from YouTube URL."""
        try:
            info = self.ydl.extract_info(url, download=False)
            return {
                "title": info.get("title"),
                "url": info.get("url"),
                "webpage_url": info.get("webpage_url"),
                "duration": info.get("duration"),
            }
        except Exception as e:
            raise Exception(f"Could not extract video info: {str(e)}")

    @app_commands.command(
        name="join",
        description="Join the voice channel you are currently in",
    )
    async def join(self, interaction: discord.Interaction):
        """Join the user's voice channel."""
        if not interaction.user.voice:
            await interaction.response.send_message(
                "❌ You need to be in a voice channel first!"
            )
            return

        voice_channel = interaction.user.voice.channel

        try:
            if interaction.guild.voice_client is not None:
                await interaction.guild.voice_client.move_to(voice_channel)
                await interaction.response.send_message(
                    f"✅ Moved to {voice_channel.mention}"
                )
            else:
                await voice_channel.connect()
                await interaction.response.send_message(
                    f"✅ Joined {voice_channel.mention}"
                )
        except Exception as e:
            await interaction.response.send_message(f"❌ Error joining voice channel: {str(e)}")

    @app_commands.command(
        name="leave",
        description="Leave the voice channel",
    )
    async def leave(self, interaction: discord.Interaction):
        """Leave the voice channel."""
        voice_client = interaction.guild.voice_client

        if voice_client is None:
            await interaction.response.send_message("❌ Bot is not in a voice channel!")
            return

        try:
            # Clear queue when leaving
            guild_id = interaction.guild_id
            if guild_id in self.music_queues:
                self.music_queues[guild_id].clear()
            if guild_id in self.now_playing:
                del self.now_playing[guild_id]

            await voice_client.disconnect()
            await interaction.response.send_message("✅ Left the voice channel")
        except Exception as e:
            await interaction.response.send_message(f"❌ Error leaving voice channel: {str(e)}")

    @app_commands.command(
        name="play",
        description="Play a song from a YouTube URL or search term",
    )
    @app_commands.describe(query="YouTube URL or search term")
    async def play(self, interaction: discord.Interaction, query: str):
        """Play a song from YouTube URL or search term."""
        await interaction.response.defer()

        # Check if user is in a voice channel
        if not interaction.user.voice:
            await interaction.followup.send(
                "❌ You need to be in a voice channel first!"
            )
            return

        voice_channel = interaction.user.voice.channel

        # Join if not already in voice
        if interaction.guild.voice_client is None:
            try:
                await voice_channel.connect()
            except Exception as e:
                await interaction.followup.send(f"❌ Error joining voice channel: {str(e)}")
                return

        # Defer to give time to fetch video info
        await interaction.followup.send("🔍 Searching for song...")

        try:
            # Extract video information
            video_info = self.extract_video_info(query)

            # Add to queue
            queue = self.get_queue(interaction.guild_id)
            queue.add(video_info)

            song_count = len(queue.queue)

            if interaction.guild.voice_client.is_playing():
                await interaction.followup.send(
                    f"✅ Added to queue: **{video_info['title']}** (Position: #{song_count})"
                )
            else:
                await self.play_next(interaction)

        except Exception as e:
            await interaction.followup.send(f"❌ Error: {str(e)}")

    @app_commands.command(
        name="pause",
        description="Pause the currently playing song",
    )
    async def pause(self, interaction: discord.Interaction):
        """Pause the currently playing song."""
        voice_client = interaction.guild.voice_client

        if voice_client is None or not voice_client.is_playing():
            await interaction.response.send_message("❌ No song is currently playing!")
            return

        voice_client.pause()
        await interaction.response.send_message("⏸️ Paused")

    @app_commands.command(
        name="resume",
        description="Resume the paused song",
    )
    async def resume(self, interaction: discord.Interaction):
        """Resume the paused song."""
        voice_client = interaction.guild.voice_client

        if voice_client is None:
            await interaction.response.send_message("❌ Bot is not in a voice channel!")
            return

        if not voice_client.is_paused():
            await interaction.response.send_message("❌ No song is paused!")
            return

        voice_client.resume()
        await interaction.response.send_message("▶️ Resumed")

    @app_commands.command(
        name="stop",
        description="Stop the currently playing song",
    )
    async def stop(self, interaction: discord.Interaction):
        """Stop the currently playing song."""
        voice_client = interaction.guild.voice_client

        if voice_client is None or not voice_client.is_playing():
            await interaction.response.send_message("❌ No song is currently playing!")
            return

        voice_client.stop()
        await interaction.response.send_message("⏹️ Stopped")

    @app_commands.command(
        name="skip",
        description="Skip the currently playing song",
    )
    async def skip(self, interaction: discord.Interaction):
        """Skip the currently playing song."""
        voice_client = interaction.guild.voice_client

        if voice_client is None or not voice_client.is_playing():
            await interaction.response.send_message("❌ No song is currently playing!")
            return

        voice_client.stop()
        await interaction.response.send_message("⏭️ Skipped to next song")

    @app_commands.command(
        name="now",
        description="Show the currently playing song",
    )
    async def now(self, interaction: discord.Interaction):
        """Show the currently playing song."""
        guild_id = interaction.guild_id

        if guild_id not in self.now_playing or self.now_playing[guild_id] is None:
            await interaction.response.send_message("❌ No song is currently playing!")
            return

        title, url = self.now_playing[guild_id]
        embed = discord.Embed(
            title="Currently Playing",
            description=f"**{title}**",
            url=url,
            color=discord.Color.blue(),
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="queue",
        description="Show the music queue",
    )
    async def show_queue(self, interaction: discord.Interaction):
        """Show the music queue."""
        guild_id = interaction.guild_id
        queue = self.get_queue(guild_id)

        if queue.is_empty():
            await interaction.response.send_message("📭 Queue is empty!")
            return

        queue_list = "\n".join(
            [f"{i + 1}. {song['title']}" for i, song in enumerate(queue.queue)]
        )

        embed = discord.Embed(
            title="Music Queue",
            description=queue_list[:2048],  # Discord limit
            color=discord.Color.purple(),
        )
        embed.set_footer(text=f"Total songs: {len(queue.queue)}")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    """Setup the music cog."""
    await bot.add_cog(Music(bot))
