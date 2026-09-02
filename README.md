# Discord Music Bot 🎵

A Python Discord bot for playing music from YouTube using slash commands. Built with `discord.py` and `yt-dlp`.

## Features ✨

- ✅ Join and leave voice channels
- ✅ Play music from YouTube URLs or search queries
- ✅ Pause and resume playback
- ✅ Skip to next song
- ✅ Stop playback
- ✅ View currently playing song
- ✅ Music queue management
- ✅ Slash commands for easy interaction
- ✅ Environment variables for secure token storage

## Prerequisites 📋

Before you start, make sure you have:

- **Python 3.8+** installed
- **FFmpeg** installed and in your system PATH
  - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
  - **macOS**: `brew install ffmpeg`
  - **Linux**: `sudo apt-get install ffmpeg`
- A **Discord Bot Token** from [Discord Developer Portal](https://discord.com/developers/applications)

## Installation 🚀

1. **Clone the repository**
   ```bash
   git clone https://github.com/tasmiafarha/discord-music-bot.git
   cd discord-music-bot
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and replace `your_discord_bot_token_here` with your actual Discord bot token

## Getting Your Discord Bot Token 🔐

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under TOKEN, click "Copy" to copy your bot token
5. Paste it in your `.env` file
6. Go to OAuth2 → URL Generator and select:
   - Scopes: `bot`
   - Permissions: `Send Messages`, `Manage Messages`, `Connect`, `Speak`, `Use Voice Activity`
7. Copy the generated URL and open it in your browser to invite the bot to your server

## Running the Bot 🎬

```bash
python bot.py
```

You should see:
```
✅ Bot is ready! Logged in as YourBotName#0000
✅ Loaded cog: music
✅ Synced X command(s)
```

## Usage 📖

Use these slash commands in Discord:

### `/join`
Join the voice channel you're currently in.
```
/join
```

### `/play`
Play a song from a YouTube URL or search term.
```
/play https://www.youtube.com/watch?v=dQw4w9WgXcQ
/play Never Gonna Give You Up Rick Astley
```

### `/pause`
Pause the currently playing song.
```
/pause
```

### `/resume`
Resume the paused song.
```
/resume
```

### `/skip`
Skip to the next song in the queue.
```
/skip
```

### `/stop`
Stop the currently playing song.
```
/stop
```

### `/now`
Show information about the currently playing song.
```
/now
```

### `/queue`
Display the music queue.
```
/queue
```

### `/leave`
Leave the voice channel.
```
/leave
```

## Project Structure 📁

```
discord-music-bot/
├── bot.py              # Main bot entry point
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your actual environment variables (not in git)
├── .gitignore          # Git ignore file
├── README.md           # This file
├── cogs/
│   ├── __init__.py
│   └── music.py        # Music commands cog
└── utils/
    ├── __init__.py
    └── queue.py        # Music queue management
```

## Configuration ⚙️

Edit `config.py` to customize:

- `BOT_PREFIX`: Bot command prefix
- `BOT_INTENTS`: Discord intents the bot uses
- `MUSIC_TIMEOUT`: Seconds before bot leaves if idle
- `MAX_QUEUE_SIZE`: Maximum songs in queue
- `DOWNLOAD_OPTIONS`: yt-dlp video download settings

## Troubleshooting 🔧

### Bot doesn't respond to commands
- Make sure the bot has the `applications.commands` scope
- Ensure the bot has permissions in the channel
- Try restarting the bot

### FFmpeg not found
- Verify FFmpeg is installed: `ffmpeg -version`
- Add FFmpeg to your system PATH
- Or specify the FFmpeg path in `config.py`

### No sound in voice channel
- Check if FFmpeg is properly installed
- Verify bot has "Speak" permission in voice channel
- Try a different YouTube video

### Token not loading from .env
- Make sure `.env` file exists in the project root
- Verify `DISCORD_TOKEN=your_token_here` format is correct
- No spaces around the `=` sign

## Dependencies 📦

- **discord.py** - Discord bot framework
- **python-dotenv** - Environment variable management
- **yt-dlp** - YouTube video extraction

## Contributing 🤝

Feel free to fork this project and submit pull requests for any improvements!

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting-🔧) section
2. Open an issue on GitHub
3. Check [discord.py documentation](https://discordpy.readthedocs.io/)

---

Made with ❤️ by [tasmiafarha](https://github.com/tasmiafarha)
