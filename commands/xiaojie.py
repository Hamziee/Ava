import discord
from discord.ext import commands
from discord import app_commands
import config
import httpx
from i18n import i18n

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

        # Add the submit cat button with a URL
        self.add_item(discord.ui.Button(label="Submit Your Cat!", style=discord.ButtonStyle.link, url="https://upload-api.hamzie.site/"))

    # Rerun button
    @discord.ui.button(label="Run the command again!", style=discord.ButtonStyle.primary)
    async def rerun_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('xiaojie', user_locale)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://services-api.hamzie.net/v1/images/xiaojie")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                
                embed = discord.Embed(
                    title=lang.title,
                    color=discord.Colour.blurple()
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION} - {lang.by}: hamzie.net/api", icon_url=config.FOOTER_ICON)

                await interaction.response.send_message(embed=embed, view=Buttons())
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            await interaction.response.send_message(content=lang.error)
        except Exception as err:
            print(f'An error occurred: {err}')
            await interaction.response.send_message(content=lang.error)

class xiaojie(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="xiaojie", description="Get your daily dose of xiaojie cat pictures!")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def xiaojie(self, interaction: discord.Interaction):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('xiaojie', user_locale)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://services-api.hamzie.net/v1/images/xiaojie")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                
                embed = discord.Embed(
                    title=lang.title,
                    color=discord.Colour.blurple()
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION} - {lang.by}: hamzie.net/api", icon_url=config.FOOTER_ICON)

                await interaction.response.send_message(embed=embed, view=Buttons())
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            await interaction.response.send_message(content=lang.error)
        except Exception as err:
            print(f'An error occurred: {err}')
            await interaction.response.send_message(content=lang.error)

async def setup(client: commands.Bot):
    await client.add_cog(xiaojie(client))
