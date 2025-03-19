import asyncio
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord import app_commands
import yt_dlp as youtube_dl
import config
from i18n import i18n

# Radio stations dictionary, alphabetically sorted with EN first
RADIO_STATIONS = {
    "en_truckersfm": {
        "url": "https://radio.truckers.fm/",
        "name": "[EN] TruckersFM",
        "description": "The #1 Hit Music Station for Truckers"
    },
    "nl_bnr": {
        "url": "https://stream.bnr.nl/bnr_mp3_128_20",
        "name": "[NL] BNR Nieuwsradio",
        "description": "24/7 het laatste nieuws, weer, verkeer en business updates"
    },
    "nl_funx_fissa": {
        "url": "https://icecast.omroep.nl/funx-dance-bb-mp3",
        "name": "[NL] FunX Fissa",
        "description": "Luister 24/7 non-stop naar de beste party tracks!"
    },
    "nl_funx_hiphop": {
        "url": "https://icecast.omroep.nl/funx-hiphop-bb-mp3",
        "name": "[NL] FunX Hip Hop",
        "description": "De beste hip-hop, R&B en urban muziek, non-stop!"
    },
    "nl_funx_nl": {
        "url": "https://icecast.omroep.nl/funx-bb-mp3",
        "name": "[NL] FunX NL",
        "description": "De beste Nederlandse hits en urban muziek, non-stop!"
    },
    "nl_slam": {
        "url": "https://stream.slam.nl/slam_mp3",
        "name": "[NL] Slam!",
        "description": "De beste dance hits en non-stop dance muziek!"
    }
}

YTDL_OPTIONS = {
    "format": "bestaudio[ext=webm]/bestaudio/best",
    "extractaudio": True,
    "audioformat": "webm",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": False,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}
ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

# Replace the get_lang_module function with this simpler version
def get_lang_module(user_id):
    user_locale = i18n.get_locale(user_id)
    return i18n.get_module('music', user_locale)

class VoiceState:
    def __init__(self, bot):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.current = None
        self.voice = None
        self.loop = False
        self.stop_next = False
        self.inactivity_task = None
        self.is_radio = False  # New flag to track if currently playing radio

    async def stop_playback(self):
        """Safely stop current playback and wait for FFMPEG to terminate."""
        if self.voice and self.voice.is_playing():
            self.voice.stop()
            # Give FFMPEG time to properly terminate
            for _ in range(3):  # Try up to 3 times
                await asyncio.sleep(0.5)
                if not self.voice.is_playing():
                    break

    async def play_next(self, interaction_channel=None):
        try:
            if not self.queue.empty() and self.is_radio:
                self.is_radio = False
                await self.stop_playback()
                if interaction_channel:
                    lang = get_lang_module(self.current["requester_id"])
                    embed = MusicCog.create_embed(
                        lang.radio_title,
                        lang.radio_stopped,
                        discord.Color.blue()
                    )
                    await interaction_channel.send(embed=embed)

            if (self.queue.empty() and not self.is_radio) or self.stop_next:
                self.current = None
                await self.start_inactivity_timeout()
                return

            if not self.is_radio:  # Only get next from queue if not radio
                self.current = await self.queue.get()
            
            # Safety check for URL
            if not self.current or "url" not in self.current:
                print("Invalid song in queue - missing URL")
                # Try the next song
                asyncio.create_task(self.play_next(interaction_channel))
                return

            # Ensure any existing playback is stopped
            await self.stop_playback()

            # Create new FFmpeg player
            audio_source = discord.FFmpegPCMAudio(self.current["url"], **FFMPEG_OPTIONS)
            
            def after_callback(error):
                if error:
                    print(f"Error in playback: {error}")
                if not self.is_radio:  # Only auto-play next for non-radio
                    coro = self.play_next(interaction_channel)
                    fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                    try:
                        fut.result()
                    except Exception as e:
                        print(f"Error in play_next callback: {e}")

            self.voice.play(audio_source, after=after_callback)

            if interaction_channel:
                await self.announce_now_playing(interaction_channel)
        except Exception as e:
            print(f"Error in play_next: {e}")
            if not self.is_radio:
                asyncio.create_task(self.play_next(interaction_channel))

    def is_playing(self):
        return self.voice.is_playing() if self.voice else False

    def clear(self):
        """Clear the queue and stop current playback."""
        self.queue = asyncio.Queue()
        self.stop_next = True
        self.is_radio = False
        asyncio.create_task(self.stop_playback())

    async def start_inactivity_timeout(self):
        """Handle leaving after inactivity or if the channel is empty."""
        if self.inactivity_task:
            self.inactivity_task.cancel()
            self.inactivity_task = None

        async def inactivity_check():
            while True:
                await asyncio.sleep(5)
                if self.voice and self.voice.channel:
                    # Get number of non-bot members in voice channel
                    members = [m for m in self.voice.channel.members if not m.bot]
                    
                    # Leave if:
                    # 1. Channel is empty (no non-bot members)
                    # 2. Not playing anything and queue is empty (for regular music)
                    if len(members) == 0 or (not self.is_radio and not self.is_playing() and self.queue.empty()):
                        print(f"Disconnecting due to {'empty channel' if len(members) == 0 else 'inactivity'}")
                        await self.voice.disconnect()
                        self.voice = None
                        self.current = None
                        self.is_radio = False
                        break
                else:
                    break
        
        self.inactivity_task = asyncio.create_task(inactivity_check())

    def reset(self):
        """Reset the voice state but keep the queue."""
        self.current = None
        self.stop_next = False
        self.is_radio = False
        if self.inactivity_task:
            self.inactivity_task.cancel()
            self.inactivity_task = None

    async def announce_now_playing(self, channel):
        """Announce the currently playing song in the specified channel."""
        if self.current:
            # Using the default en_US language for announcements
            lang = get_lang_module(self.current["requester_id"])
            embed = MusicCog.create_embed(
                lang.now_playing,
                f"{lang.song_info.format(title=self.current['title'], url=self.current['url'], author=self.current['author'], requester=self.current['requester'], duration=self.current['duration'])}",
                discord.Color.green()
            )
            await channel.send(embed=embed)

class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, guild_id):
        if guild_id not in self.voice_states:
            self.voice_states[guild_id] = VoiceState(self.bot)
        return self.voice_states[guild_id]

    async def join_channel(self, interaction):
        # Get language for this user
        lang = get_lang_module(interaction.user.id)
        
        if not interaction.user.voice or not interaction.user.voice.channel:
            embed = self.create_embed(
                lang.error,
                lang.must_be_in_voice,
                discord.Color.red(),
                lang
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return None
            
        channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client
        
        if voice_client and voice_client.channel != channel:
            embed = self.create_embed(
                lang.error,
                lang.already_in_another_voice,
                discord.Color.red(),
                lang
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return None
            
        if not voice_client:
            voice_client = await channel.connect()
            state = self.get_voice_state(interaction.guild.id)
            state.voice = voice_client
            state.reset()
        
        return interaction.guild.voice_client
    
    @app_commands.command(name="nowplaying", description="See what's currently playing.")
    async def nowplaying(self, interaction: discord.Interaction):
        # Get language for this user
        lang = get_lang_module(interaction.user.id)
        
        state = self.get_voice_state(interaction.guild.id)
        if state.current:
            embed = self.create_embed(
                lang.now_playing,
                lang.song_info.format(
                    title=state.current['title'],
                    url=state.current['url'],
                    author=state.current['author'],
                    requester=state.current['requester'],
                    duration=state.current['duration']
                ),
                discord.Color.green(),
                lang
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = self.create_embed(
                lang.now_playing,
                lang.no_music_playing,
                discord.Color.orange(),
                lang
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @staticmethod
    def create_embed(title, description, color=discord.Color.blue(), lang=None):
        """Create an embed with a footer using the provided language module."""
        embed = discord.Embed(title=title, description=description, color=color)
        
        # Use the provided language module or default to getting a new one
        if not lang:
            lang = i18n.get_module('music', 'en_US')
            
        embed.set_footer(
            text=f"Ava | {lang.version}: {config.AVA_VERSION} - {lang.footer_extra}",
            icon_url=config.FOOTER_ICON
        )
        return embed

    async def search_song(self, query):
        """Search for a song using yt_dlp in a separate thread."""
        try:
            data = await asyncio.to_thread(ytdl.extract_info, query, download=False)
            if not data:
                return None
                
            # Validate data structure
            if 'entries' in data:
                # Make sure entries isn't empty
                if not data['entries']:
                    return None
                # Check first entry to make sure it has URL
                if not data['entries'][0].get('url'):
                    return None
            elif not data.get('url'):
                return None
                
            return data
        except Exception as e:
            print(f"Error during search: {e}")
            return None

    @app_commands.command(name="play", description="Play a song or add to the queue.")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    async def play(self, interaction: discord.Interaction, query: str):
        lang = get_lang_module(interaction.user.id)
        
        voice_client = await self.join_channel(interaction)
        if not voice_client:
            return

        state = self.get_voice_state(interaction.guild.id)
        state.voice = voice_client
        state.stop_next = False

        embed = self.create_embed(
            lang.searching, 
            lang.searching_for.format(query=query),
            discord.Color.blue(),
            lang
        )
        await interaction.response.send_message(embed=embed)

        data = await self.search_song(query)
        if not data:
            embed = self.create_embed(
                lang.error,
                lang.no_results,
                discord.Color.red(),
                lang
            )
            await interaction.followup.send(embed=embed)
            return

        try:
            entries = []
            if 'entries' in data and data['entries']:
                entries = [entry for entry in data['entries'] if entry and 'url' in entry]
            elif data and 'url' in data:
                entries = [data]
                
            if not entries:
                embed = self.create_embed(
                    lang.error,
                    lang.invalid_song_data,
                    discord.Color.red(),
                    lang
                )
                await interaction.followup.send(embed=embed)
                return

            for entry in entries:
                # Validate entry has required fields
                if not entry or 'url' not in entry:
                    continue
                    
                song = {
                    "url": entry["url"],
                    "title": entry.get("title", "Unknown Title"),
                    "duration": entry.get("duration", "Unknown"),
                    "author": entry.get("uploader", "Unknown"),
                    "requester": interaction.user.display_name,
                    "requester_id": interaction.user.id  # Store requester's ID for language lookup
                }
                await state.queue.put(song)

                embed = self.create_embed(
                    lang.song_added,
                    lang.song_info.format(
                        title=song['title'],
                        url=song['url'],
                        author=song['author'],
                        requester=song['requester'],
                        duration=song['duration']
                    ),
                    discord.Color.blue(),
                    lang
                )
                await interaction.followup.send(embed=embed)

            # If radio is playing or not playing anything, start playing from queue
            if state.is_radio or not state.is_playing():
                await state.play_next(interaction.channel)
        except Exception as e:
            print(f"Play command error: {e}")  # Better logging
            embed = self.create_embed(
                lang.error,
                lang.processing_error.format(error=str(e)),
                discord.Color.red(),
                lang
            )
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="skip", description="Skip the current song.")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    async def skip(self, interaction: discord.Interaction):
        # Get language for this user
        lang = get_lang_module(interaction.user.id)
        
        state = self.get_voice_state(interaction.guild.id)
        if state.voice and state.voice.is_playing():
            state.voice.stop()
            embed = self.create_embed(lang.skipped, lang.skipped_success, discord.Color.blue(), lang)
            await interaction.response.send_message(embed=embed)
        else:
            embed = self.create_embed(lang.error, lang.no_music_playing, discord.Color.red(), lang)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="queue", description="View the current song queue.")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    async def queue(self, interaction: discord.Interaction, page: int = 1):
        # Get language for this user
        lang = get_lang_module(interaction.user.id)
        
        state = self.get_voice_state(interaction.guild.id)
        if state.queue.empty():
            embed = self.create_embed(lang.queue_title, lang.queue_empty, discord.Color.orange(), lang)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        queue = list(state.queue._queue)
        items_per_page = 10
        max_pages = (len(queue) + items_per_page - 1) // items_per_page

        if page < 1 or page > max_pages:
            embed = self.create_embed(
                lang.error, 
                lang.invalid_page.format(max_pages=max_pages),
                discord.Color.red(),
                lang
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        start = (page - 1) * items_per_page
        end = start + items_per_page
        queue_str = "\n".join(
            [
                f"{i+1}. {lang.song_info.format(title=song['title'], url=song['url'], author=song['author'], requester=song['requester'], duration=song['duration'])}"
                for i, song in enumerate(queue[start:end], start=start)
            ]
        )
        embed = self.create_embed(
            lang.queue_title, 
            lang.queue_page.format(page=page, max_pages=max_pages, queue_str=queue_str),
            discord.Color.blue(),
            lang
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leave", description="Leave the voice channel and clear the queue.")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    async def leave(self, interaction: discord.Interaction):
        # Get language for this user
        lang = get_lang_module(interaction.user.id)
        
        state = self.get_voice_state(interaction.guild.id)
        if state.voice:
            await state.voice.disconnect()
            state.clear()
            self.voice_states.pop(interaction.guild.id, None)
            embed = self.create_embed(
                lang.disconnected,
                lang.disconnect_success,
                discord.Color.blue(),
                lang
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = self.create_embed(lang.error, lang.not_in_voice, discord.Color.red(), lang)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="radio", description="Play a radio station")
    @app_commands.allowed_installs(guilds=True, users=False)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    @app_commands.choices(station=[
        app_commands.Choice(name="[EN] TruckersFM", value="en_truckersfm"),
        app_commands.Choice(name="[NL] BNR Nieuwsradio", value="nl_bnr"),
        app_commands.Choice(name="[NL] FunX Fissa", value="nl_funx_fissa"),
        app_commands.Choice(name="[NL] FunX Hip Hop", value="nl_funx_hiphop"),
        app_commands.Choice(name="[NL] FunX NL", value="nl_funx_nl"),
        app_commands.Choice(name="[NL] Slam!", value="nl_slam")
    ])
    async def radio(self, interaction: discord.Interaction, station: str):
        lang = get_lang_module(interaction.user.id)
        
        if station not in RADIO_STATIONS:
            embed = self.create_embed(
                lang.error,
                lang.radio_not_found,
                discord.Color.red(),
                lang
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        voice_client = await self.join_channel(interaction)
        if not voice_client:
            return

        state = self.get_voice_state(interaction.guild.id)
        
        # If we were playing music before, show transition message
        if not state.is_radio and (state.is_playing() or not state.queue.empty()):
            embed = self.create_embed(
                lang.radio_title,
                lang.radio_switched,
                discord.Color.blue(),
                lang
            )
            await interaction.channel.send(embed=embed)

        state.voice = voice_client
        state.stop_next = False
        state.is_radio = True

        # Clear current queue when switching to radio
        state.queue = asyncio.Queue()
        await state.stop_playback()

        # Set up radio stream
        radio_info = RADIO_STATIONS[station]
        state.current = {
            "url": radio_info["url"],
            "title": radio_info["name"],
            "duration": "24/7",
            "author": radio_info["description"],
            "requester": interaction.user.display_name,
            "requester_id": interaction.user.id
        }

        embed = self.create_embed(
            lang.radio_title,
            lang.radio_playing.format(name=radio_info["name"], description=radio_info["description"]),
            discord.Color.blue(),
            lang
        )
        await interaction.response.send_message(embed=embed)
        
        # Start the inactivity check immediately for radio
        await state.start_inactivity_timeout()
        
        # Start playing the radio
        await state.play_next(interaction.channel)

async def setup(bot):
    await bot.add_cog(MusicCog(bot))