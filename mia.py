import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import time
import platform
from cogwatch import watch
try:
    import config
except:
    print(Fore.RED + Style.BRIGHT + "Config file could not be found, please refer to the setup instructions in the readme.md file!" + Fore.RESET)
    exit()
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

    # Load, Reload and Unload commands
    # Load command
    @commands.command()
    async def load(self, ctx, cog: str):
        if ctx.message.author.id == config.OWNER_ID:
            try:
                await self.load_extension(f"{config.COMMANDS_DIRECTORY}.{cog}")
                await ctx.reply(f"Loaded {cog}.py cog.")
            except Exception as e:
                print(e)
                await ctx.reply("Error.")
        else:
            await ctx.reply("Insufficient permissions! Only the developer(s) can load commands.")

    # Reload command
    @commands.command()
    async def reload(self, ctx, cog: str):
        if ctx.message.author.id == config.OWNER_ID:
            try:
                await self.reload_extension(f"{config.COMMANDS_DIRECTORY}.{cog}")
                await ctx.reply(f"Reloaded {cog}.py cog.")
            except Exception as e:
                print(e)
                await ctx.reply("Error.")
        else:
            await ctx.reply("Insufficient permissions! Only the developer(s) can reload commands.")

    # Reload all command
    @commands.command()
    async def reloadall(self, ctx):
        if ctx.message.author.id == config.OWNER_ID:
            try:
                for ext in self.cogslist:
                    await self.load_extension(ext)
                await ctx.reply("Reloaded all commands.")
            except Exception as e:
                print(e)
                await ctx.reply("Error.")
        else:
            await ctx.reply("Insufficient permissions! Only the developer(s) can reload commands.")

    # Unload command
    @commands.command()
    async def unload(self, ctx, cog: str):
        if ctx.message.author.id == config.OWNER_ID:
            try:
                await self.unload_extension(f"{config.COMMANDS_DIRECTORY}.{cog}")
                await ctx.reply(f"Unloaded {cog}.py cog.")
            except Exception as e:
                print(e)
                await ctx.reply("Error.")
        else:
            await ctx.reply("Insufficient permissions! Only the developer(s) can unload commands.")

    #### #### #### #### ####

client = Client()

client.run(config.TOKEN)