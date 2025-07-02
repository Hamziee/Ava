import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import platform
from cogwatch import watch
import os
from typing import List
import requests
import config

if config.CONFIG_VERSION != 5:
    raise ValueError(Fore.RED + Style.BRIGHT + "Config file version is outdated, please use the new config format and try again." + Fore.RESET)
elif config.TOKEN == 'Put your Discord bot token here.':
    raise ValueError(Fore.RED + Style.BRIGHT + "Bot token is incorrect, please change it to the correct token in the config file." + Fore.RESET)
elif config.THECATAPI_KEY == 'your thecatapi key here':
    print(Fore.YELLOW + Style.BRIGHT + "Warning: TheCatAPI key is not set. The cats command will be disabled. To hide this warning, move cats.py to the disabled_commands folder." + Fore.RESET)

class Client(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or(config.PREFIX), intents=discord.Intents().all())
        self.cogslist: List[str] = self._list_cogs_files(config.COMMANDS_DIRECTORY)

    def _list_cogs_files(self, directory: str) -> List[str]:
        cog_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    cog_files.append(f"{config.COMMANDS_DIRECTORY}." + file[:-3])
        return cog_files
    
    async def setup_hook(self) -> None:
        for ext in self.cogslist:
            await self.load_extension(ext)

    async def _check_version(self) -> None:
        url = "https://services-cdn.hamzie.net/Ava/VRC/core.txt"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                remote_version = response.text.strip()
                if config.AVA_VERSION != remote_version:
                    print(Fore.RED + Style.BRIGHT + f"Version mismatch! Local: {config.AVA_VERSION}, Remote: {remote_version}\nDownload the latest version at: https://github.com/Hamziee/Ava" + Fore.RESET)
                else:
                    print("Ava up-to-date!")
        except Exception as e:
            print(f"Failed to fetch latest Ava version: {e}")

    @watch(path=config.COMMANDS_DIRECTORY, preload=True)
    async def on_ready(self) -> None:
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Ava version " + Fore.YELLOW + str(config.AVA_VERSION))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await self.tree.sync()
        print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")
        await self.change_presence(activity=discord.Game(name=config.STATUS))
        print(prfx + " Discord " + Fore.YELLOW + "Presence(s) loaded.")
        await self._check_version()

client = Client()
client.run(config.TOKEN)
