import discord
from discord.ext import commands
from discord import app_commands
import httpx
from datetime import datetime
import config
from userLocale import getLang
import importlib

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

        # Add the submit cat button with a URL
        self.add_item(discord.ui.Button(label="Submit Your Cat!", style=discord.ButtonStyle.link, url="https://upload-api.hamzie.site/"))

    @discord.ui.button(label="Run the command again!", style=discord.ButtonStyle.primary)
    async def rerun_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ### LANG SECTION ###
        user_locale = getLang(interaction.user.id)
        lang_module = f"lang.dogs.{user_locale}"
        try:
            lang = importlib.import_module(lang_module)
        except ModuleNotFoundError:
            import lang.dogs.en_US as lang
            print(f"[!] Error loading language file. Defaulting to en_US | File not found: {lang_module} | User locale: {user_locale}")
        ### END OF LANG SECTION ###
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://dog.ceo/api/breeds/image/random")
                response.raise_for_status()
                data = response.json()
                image_url = data["message"]
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title=lang.title
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: dog.ceo/dog-api/", icon_url=config.FOOTER_ICON)

            await interaction.response.send_message(embed=embed, view=Buttons())
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

class dogs(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="dogs", description="Get your daily dose of dogs :)")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def dogs(self, interaction: discord.Interaction):
        ### LANG SECTION ###
        user_locale = getLang(interaction.user.id)
        lang_module = f"lang.dogs.{user_locale}"
        try:
            lang = importlib.import_module(lang_module)
        except ModuleNotFoundError:
            import lang.dogs.en_US as lang
            print(f"[!] Error loading language file. Defaulting to en_US | File not found: {lang_module} | User locale: {user_locale}")
        ### END OF LANG SECTION ###
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://dog.ceo/api/breeds/image/random")
                response.raise_for_status()
                data = response.json()
                image_url = data["message"]
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title=lang.title
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: dog.ceo/dog-api/", icon_url=config.FOOTER_ICON)

                await interaction.response.send_message(embed=embed, view=Buttons())
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(dogs(client))