import discord
from discord.ext import commands
from discord import app_commands
import httpx
import config
from userLocale import getLang
import importlib

class Slap(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="slap", description="Slap someone who deserves it!")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.rename(member='person')
    async def slap(self, interaction: discord.Interaction, member: discord.User):
        ### LANG SECTION ###
        user_locale = getLang(interaction.user.id)
        lang_module = f"lang.slap.{user_locale}"
        try:
            lang = importlib.import_module(lang_module)
        except ModuleNotFoundError:
            import lang.slap.en_US as lang
            print(f"[!] Error loading language file. Defaulting to en_US | File not found: {lang_module} | User locale: {user_locale}")
        ### END OF LANG SECTION ###
        try:
            async with httpx.AsyncClient() as client:
                if member.id == interaction.user.id:
                    response = await client.get("https://api.hamzie.site/v1/gifs/hug")
                    response.raise_for_status()
                    data = response.json()
                    image_url = data["link"]
                    embed = discord.Embed(
                        color=discord.Colour.blurple()
                    )
                    embed.set_image(url=image_url)
                    embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION} - {lang.by}: api.hamzie.site", icon_url=config.FOOTER_ICON)
                    await interaction.response.send_message(content=lang.slap_toself, embed=embed)
                    return
                if member.id == config.BOT_ID:
                    response = await client.get("https://api.hamzie.site/v1/gifs/hug")
                    response.raise_for_status()
                    data = response.json()
                    image_url = data["link"]
                    embed = discord.Embed(
                        color=discord.Colour.blurple()
                    )
                    embed.set_image(url=image_url)
                    embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION} - {lang.by}: api.hamzie.site", icon_url=config.FOOTER_ICON)
                    await interaction.response.send_message(content=lang.slap_toava, embed=embed)
                    return
                response = await client.get("https://api.hamzie.site/v1/gifs/slap")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    description=f"{interaction.user.mention} {lang.gives_slap} {member.mention}"
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION} - {lang.by}: api.hamzie.site", icon_url=config.FOOTER_ICON)
                await interaction.response.send_message(embed=embed)
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')
        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(Slap(client))
