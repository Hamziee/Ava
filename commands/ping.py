import discord
from discord.ext import commands
from discord import app_commands
import time
import config
import httpx
from userLocale import getLang
import importlib

class ping(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="ping", description="Calculate current latency.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ping(self, interaction: discord.Interaction):
        ### LANG SECTION ###
        user_locale = getLang(interaction.user.id)
        lang_module = f"lang.ping.{user_locale}"
        try:
            lang = importlib.import_module(lang_module)
        except ModuleNotFoundError:
            import lang.ping.en_US as lang
            print(f"[!] Error loading language file. Defaulting to en_US | File not found: {lang_module} | User locale: {user_locale}")
        ### END OF LANG SECTION ###
        try:
            start = time.time()
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=lang.pinging,
                description='🤔')
            embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.response.send_message(embed=embed)
            end = time.time()
            duration = round((end - start) * 100)
            durationtext = f"{duration}ms"
            try:
                startapi = time.time()
                async with httpx.AsyncClient() as client:
                    response = await client.get("https://api.hamzie.site/v1/gifs/hug")
                    response.raise_for_status()
                endapi = time.time()
                durationapi = round((endapi - startapi) * 100)
                durationapitext = f"{durationapi}ms"
            except:
                durationapitext = lang.noresponse
            embed = discord.Embed(
                title=lang.pong, 
                description=f"{lang.discordapi}: {durationtext}\n{lang.hamzieapi}: {durationapitext} \n\n{lang.whatmean}", 
                color=discord.Color.blurple())
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content=lang.error)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(ping(client))