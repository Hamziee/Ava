import asyncio
import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord import app_commands
import yt_dlp as youtube_dl
import config

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

        self.voice.play(
            discord.FFmpegPCMAudio(self.current["url"], **FFMPEG_OPTIONS),
            after=lambda _: asyncio.run_coroutine_threadsafe(self.play_next(interaction_channel), self.bot.loop).result(),
        )

        if interaction_channel:
            await self.announce_now_playing(interaction_channel)


    def is_playing(self):
        return self.voice.is_playing() if self.voice else False

    def clear(self):
        self.queue = asyncio.Queue()
        self.stop_next = True
        if self.voice and self.voice.is_playing():
            self.voice.stop()

    async def start_inactivity_timeout(self):
        """Handle leaving after 1 minute of inactivity or if the channel is empty."""
        if self.inactivity_task:
            self.inactivity_task.cancel()

        async def inactivity_check():
            await asyncio.sleep(5)
            if self.voice:
                if not self.is_playing() and self.queue.empty():
                    await self.voice.disconnect()
                    self.clear()
                    
        self.inactivity_task = asyncio.create_task(inactivity_check())

    async def announce_now_playing(self, channel):
        """Announce the currently playing song in the specified channel."""
        if self.current:
            embed = MusicCog.create_embed(
                "Now Playing",
                f"[**{self.current['title']}**]({self.current['url']}) by **{self.current['author']}**\n"
                f"Requested by **{self.current['requester']}** | Duration: {self.current['duration']}s",
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
        if not interaction.user.voice or not interaction.user.voice.channel:
            embed = self.create_embed(
                "Error",
                "You must be in a voice channel!",
                discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return None
        channel = interaction.user.voice.channel
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.channel != channel:
            embed = self.create_embed(
                "Error",
                "I'm already in another voice channel.",
                discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return None
        if not voice_client:
            await channel.connect()
        return interaction.guild.voice_client
    
    @app_commands.command(name="nowplaying", description="See what's currently playing.")
    async def nowplaying(self, interaction: discord.Interaction):
        state = self.get_voice_state(interaction.guild.id)
        if state.current:
            embed = self.create_embed(
                "Now Playing",
                f"[**{state.current['title']}**]({state.current['url']}) by **{state.current['author']}**\n"
                f"Requested by **{state.current['requester']}** | Duration: {state.current['duration']}s",
                discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = self.create_embed(
                "Now Playing",
                "No music is currently playing.",
                discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @staticmethod
    def create_embed(title, description, color=discord.Color.blue()):
        """Create an embed with a footer."""
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(
            text=config.FOOTER_TXT + f" - Entirly rewritten Play command for speed & audio quality.",
            icon_url=config.FOOTER_ICON
        )
        return embed

    async def search_song(self, query):
        """Search for a song using yt_dlp in a separate thread."""
        try:
            return await asyncio.to_thread(ytdl.extract_info, query, download=False)
        except Exception as e:
            print(f"Error during search: {e}")
            return None

    @app_commands.command(name="play", description="Play a song or add to the queue.")
    async def play(self, interaction: discord.Interaction, query: str):
        voice_client = await self.join_channel(interaction)
        if not voice_client:
            return

        state = self.get_voice_state(interaction.guild.id)

        embed = self.create_embed("Searching", f"Searching for `{query}`...")
        await interaction.response.send_message(embed=embed)

        data = await self.search_song(query)
        if not data:
            embed = self.create_embed(
                "Error",
                "Could not find any results for your query.",
                discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return

        try:
            if 'entries' in data:
                entries = data['entries']
            else:
                entries = [data]

            for entry in entries:
                song = {
                    "url": entry["url"],
                    "title": entry.get("title", "Unknown Title"),
                    "duration": entry.get("duration", "Unknown"),
                    "author": entry.get("uploader", "Unknown"),
                    "requester": interaction.user.display_name,
                }
                await state.queue.put(song)

                embed = self.create_embed(
                    "Song Added",
                    f"[**{song['title']}**]({song['url']}) by **{song['author']}**\n"
                    f"Requested by **{song['requester']}** | Duration: {song['duration']}s"
                )
                await interaction.followup.send(embed=embed)

            if not state.is_playing():
                state.voice = voice_client
                await state.play_next(interaction.channel)
        except Exception as e:
            embed = self.create_embed(
                "Error",
                f"An error occurred while processing the song: {e}",
                discord.Color.red()
            )
            await interaction.followup.send(embed=embed)


    @app_commands.command(name="skip", description="Skip the current song.")
    async def skip(self, interaction: discord.Interaction):
        state = self.get_voice_state(interaction.guild.id)
        if state.voice and state.voice.is_playing():
            state.voice.stop()
            embed = self.create_embed("Skipped", "Skipped the current song.")
            await interaction.response.send_message(embed=embed)
        else:
            embed = self.create_embed("Error", "No music is currently playing.", discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="queue", description="View the current song queue.")
    async def queue(self, interaction: discord.Interaction, page: int = 1):
        state = self.get_voice_state(interaction.guild.id)
        if state.queue.empty():
            embed = self.create_embed("Queue", "The queue is empty.", discord.Color.orange())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        queue = list(state.queue._queue)
        items_per_page = 10
        max_pages = (len(queue) + items_per_page - 1) // items_per_page

        if page < 1 or page > max_pages:
            embed = self.create_embed("Error", f"Invalid page. Please select a page between 1 and {max_pages}.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        start = (page - 1) * items_per_page
        end = start + items_per_page
        queue_str = "\n".join(
            [
                f"{i+1}. [**{song['title']}**]({song['url']}) by **{song['author']}**\n"
                f"Requested by **{song['requester']}** | Duration: {song['duration']}s"
                for i, song in enumerate(queue[start:end], start=start)
            ]
        )
        embed = self.create_embed("Queue", f"**Page {page}/{max_pages}**\n\n{queue_str}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leave", description="Leave the voice channel and clear the queue.")
    async def leave(self, interaction: discord.Interaction):
        state = self.get_voice_state(interaction.guild.id)
        if state.voice:
            await state.voice.disconnect()
            state.clear()
            self.voice_states.pop(interaction.guild.id, None)
            embed = self.create_embed(
                "Disconnected",
                "Left the voice channel and cleared the queue."
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = self.create_embed("Error", "I'm not in a voice channel.", discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(MusicCog(bot))