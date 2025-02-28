import asyncio
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord import app_commands
import yt_dlp as youtube_dl
import config
from userLocale import getLang
import importlib

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

# Function to get language module for a user
def get_lang_module(user_id):
    user_locale = getLang(user_id)
    lang_module = f"lang.music.{user_locale}"
    try:
        return importlib.import_module(lang_module)
    except ModuleNotFoundError:
        import lang.music.en_US as lang
        print(f"[!] Error loading language file. Defaulting to en_US | File not found: {lang_module} | User locale: {user_locale}")
        return lang

class VoiceState:
    def __init__(self, bot):
        self.bot = bot
        self.queue = asyncio.Queue()
        self.current = None
        self.voice = None
        self.loop = False
        self.stop_next = False
        self.inactivity_task = None

    async def play_next(self, interaction_channel=None):
        if self.queue.empty() or self.stop_next:
            self.current = None
            await self.start_inactivity_timeout()
            return

        self.current = await self.queue.get()
        
        # Safety check for URL
        if not self.current or "url" not in self.current:
            print("Invalid song in queue - missing URL")
            # Try the next song
            asyncio.create_task(self.play_next(interaction_channel))
            return

        try:
            self.voice.play(
                discord.FFmpegPCMAudio(self.current["url"], **FFMPEG_OPTIONS),
                after=lambda _: asyncio.run_coroutine_threadsafe(self.play_next(interaction_channel), self.bot.loop).result(),
            )

            if interaction_channel:
                await self.announce_now_playing(interaction_channel)
        except Exception as e:
            print(f"Error playing song: {e}")
            # Try the next song
            asyncio.create_task(self.play_next(interaction_channel))

    def is_playing(self):
        return self.voice.is_playing() if self.voice else False

    def clear(self):
        self.queue = asyncio.Queue()
        self.stop_next = True
        if self.voice and self.voice.is_playing():
            self.voice.stop()

    async def start_inactivity_timeout(self):
        """Handle leaving after inactivity or if the channel is empty."""
        if self.inactivity_task:
            self.inactivity_task.cancel()
            self.inactivity_task = None  # Ensure it's set to None

        async def inactivity_check():
            await asyncio.sleep(5)
            if self.voice:
                if not self.is_playing() and self.queue.empty():
                    await self.voice.disconnect()
                    self.voice = None  # Reset the voice client reference
                    self.current = None
        
        self.inactivity_task = asyncio.create_task(inactivity_check())

    def reset(self):
        """Reset the voice state but keep the queue."""
        self.current = None
        self.stop_next = False
        if self.inactivity_task:
            self.inactivity_task.cancel()
            self.inactivity_task = None

    async def announce_now_playing(self, channel):
        """Announce the currently playing song in the specified channel."""
        if self.current:
            # Using the default en_US language for announcements
            import lang.music.en_US as lang
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
                discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return None
            
        channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client
        
        if voice_client and voice_client.channel != channel:
            embed = self.create_embed(
                lang.error,
                lang.already_in_another_voice,
                discord.Color.red()
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
                discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = self.create_embed(
                lang.now_playing,
                lang.no_music_playing,
                discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @staticmethod
    def create_embed(title, description, color=discord.Color.blue()):
        """Create an embed with a footer."""
        embed = discord.Embed(title=title, description=description, color=color)
        
        # Using the default language for footer
        import lang.music.en_US as lang
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
    async def play(self, interaction: discord.Interaction, query: str):
        # Get language for this user
        lang = get_lang_module(interaction.user.id)
        
        voice_client = await self.join_channel(interaction)
        if not voice_client:
            return

        state = self.get_voice_state(interaction.guild.id)
        state.voice = voice_client
        state.stop_next = False

        embed = self.create_embed(
            lang.searching, 
            lang.searching_for.format(query=query)
        )
        await interaction.response.send_message(embed=embed)

        data = await self.search_song(query)
        if not data:
            embed = self.create_embed(
                lang.error,
                lang.no_results,
                discord.Color.red()
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
                    discord.Color.red()
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
                    )
                )
                await interaction.followup.send(embed=embed)

            if not state.is_playing():
                await state.play_next(interaction.channel)
        except Exception as e:
            print(f"Play command error: {e}")  # Better logging
            embed = self.create_embed(
                lang.error,
                lang.processing_error.format(error=str(e)),
                discord.Color.red()
            )
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="skip", description="Skip the current song.")
    async def skip(self, interaction: discord.Interaction):
        # Get language for this user
        lang = get_lang_module(interaction.user.id)
        
        state = self.get_voice_state(interaction.guild.id)
        if state.voice and state.voice.is_playing():
            state.voice.stop()
            embed = self.create_embed(lang.skipped, lang.skipped_success)
            await interaction.response.send_message(embed=embed)
        else:
            embed = self.create_embed(lang.error, lang.no_music_playing, discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="queue", description="View the current song queue.")
    async def queue(self, interaction: discord.Interaction, page: int = 1):
        # Get language for this user
        lang = get_lang_module(interaction.user.id)
        
        state = self.get_voice_state(interaction.guild.id)
        if state.queue.empty():
            embed = self.create_embed(lang.queue_title, lang.queue_empty, discord.Color.orange())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        queue = list(state.queue._queue)
        items_per_page = 10
        max_pages = (len(queue) + items_per_page - 1) // items_per_page

        if page < 1 or page > max_pages:
            embed = self.create_embed(
                lang.error, 
                lang.invalid_page.format(max_pages=max_pages)
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
            lang.queue_page.format(page=page, max_pages=max_pages, queue_str=queue_str)
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leave", description="Leave the voice channel and clear the queue.")
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
                lang.disconnect_success
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = self.create_embed(lang.error, lang.not_in_voice, discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(MusicCog(bot))