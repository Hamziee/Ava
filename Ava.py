import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import platform
from cogwatch import watch
try:
    import config
except:
    raise ValueError(Fore.RED + Style.BRIGHT + "Config file could not be found, please refer to the setup instructions in the readme.md file!" + Fore.RESET)
import os

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(config.PREFIX), intents=discord.Intents().all())

        def list_cogs_files(directory):
            cog_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".py"):
                        cog_files.append(f"{config.COMMANDS_DIRECTORY}." + file[:-3])
            return cog_files

        cogs_directory = config.COMMANDS_DIRECTORY
        cog_files = list_cogs_files(cogs_directory)
        self.cogslist = cog_files
    
    async def setup_hook(self):
      for ext in self.cogslist:
        await self.load_extension(ext)

    @watch(path=config.COMMANDS_DIRECTORY, preload=True)
    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await self.tree.sync()
        print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")
        await self.change_presence(activity=discord.Game(name=config.STATUS))
        print(prfx + " Discord " + Fore.YELLOW + "Presence(s) loaded.")

client = Client()

client.run(config.TOKEN)
