import asyncio
import functools
import itertools
import math
import random

import discord
import yt_dlp as youtube_dl
from async_timeout import timeout
from discord.ext import commands
from discord import app_commands

import config

PREFIX = config.PREFIX
AVA_VERSION = config.AVA_VERSION

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, interaction: discord.Interaction, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)
        self.requester = interaction.user
        self.channel = interaction.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, interaction: discord.Interaction, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError(f"Couldn't find anything that matches `{search}`")

        if 'entries' not in data:
            process_info = data
        else:
            process_info = next((entry for entry in data['entries'] if entry), None)
            if process_info is None:
                raise YTDLError(f"Couldn't find anything that matches `{search}`")

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError(f"Couldn't fetch `{webpage_url}`")

        info = processed_info if 'entries' not in processed_info else next((entry for entry in processed_info['entries']), None)

        return cls(interaction, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration_str = []
        if days > 0:
            duration_str.append(f'{days} days')
        if hours > 0:
            duration_str.append(f'{hours} hours')
        if minutes > 0:
            duration_str.append(f'{minutes} minutes')
        if seconds > 0:
            duration_str.append(f'{seconds} seconds')

        return ', '.join(duration_str)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description=f'```css\n{self.source.title}\n```',
                               color=16202876)
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value=f'[{self.source.uploader}]({self.source.uploader_url})')
                 .set_footer(text=f"Ava | version: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        return list(itertools.islice(self._queue, item.start, item.stop, item.step)) if isinstance(item, slice) else self._queue[item]

    def __iter__(self):
        return iter(self._queue)

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, interaction: discord.Interaction):
        self.bot = bot
        self.interaction = interaction

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 1
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, interaction: discord.Interaction):
        state = self.voice_states.get(interaction.guild.id)
        if not state:
            state = VoiceState(self.bot, interaction)
            self.voice_states[interaction.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    async def cog_before_invoke(self, interaction: discord.Interaction):
        interaction.voice_state = self.get_voice_state(interaction)

    async def cog_command_error(self, interaction: discord.Interaction, error: commands.CommandError):
        await interaction.response.send_message(f"An error occurred: {str(error)}", ephemeral=True)

    @app_commands.command(name="join", description="Joins a voice channel.")
    async def _join(self, interaction: discord.Interaction):
        destination = interaction.user.voice.channel
        if interaction.voice_state.voice:
            await interaction.voice_state.voice.move_to(destination)
            return

        interaction.voice_state.voice = await destination.connect()
        await interaction.response.send_message("Joined the channel.", ephemeral=True)

    @app_commands.command(name="leave", description="Leaves the voice channel and clears the queue.")
    async def _leave(self, interaction: discord.Interaction):
        if not interaction.voice_state.voice:
            return await interaction.response.send_message("Not connected to any voice channel.", ephemeral=True)

        await interaction.voice_state.stop()
        del self.voice_states[interaction.guild.id]
        await interaction.response.send_message("Disconnected.", ephemeral=True)

    @app_commands.command(name="play", description="Plays a song or adds it to the queue.")
    async def _play(self, interaction: discord.Interaction, *, search: str):
        async with interaction.channel.typing():
            try:
                source = await YTDLSource.create_source(interaction, search, loop=self.bot.loop)
            except YTDLError as e:
                await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)
            else:
                song = Song(source)
                await interaction.voice_state.songs.put(song)
                await interaction.response.send_message(f"Added {str(source)} to the queue.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))
