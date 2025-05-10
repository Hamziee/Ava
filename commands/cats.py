import discord
from discord.ext import commands
from discord import app_commands
from colorama import Back, Fore, Style
import httpx
import config
from i18n import i18n

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Run the command again!", style=discord.ButtonStyle.primary)
    async def rerun_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('cats', user_locale)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.thecatapi.com/v1/images/search", headers={"x-api-key": config.THECATAPI_KEY})
                data = response.json()
                image_url = data[0]['url']

            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=lang.title,
                description=lang.description
            )
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION} - {lang.by}: thecatapi.com", icon_url=config.FOOTER_ICON)

            await interaction.response.send_message(embed=embed, view=Buttons())
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')


class cats(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="cats", description="Get your daily dose of cat pictures!")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def cats(self, interaction: discord.Interaction):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('cats', user_locale)

        if config.THECATAPI_KEY == 'your thecatapi key here':
            await interaction.response.send_message(content=lang.noapikey)
            return

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.thecatapi.com/v1/images/search", headers={"x-api-key": config.THECATAPI_KEY})
                response.raise_for_status()
                data = response.json()

            if data and len(data) > 0:
                image_url = data[0]["url"]
                image_id = data[0]["id"]

                embed = discord.Embed(color=discord.Colour.blurple())
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION} | {lang.by}: TheCatAPI", icon_url=config.FOOTER_ICON)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(content=lang.error)
        except Exception as e:
            print(e)
            await interaction.followup.send(content=lang.error)

async def setup(client: commands.Bot):
    await client.add_cog(cats(client))