import discord
from discord.ext import commands
from discord import app_commands
import httpx
from datetime import datetime
import config

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

        # Add the submit cat button with a URL
        self.add_item(discord.ui.Button(label="Submit Your Cat!", style=discord.ButtonStyle.link, url="https://upload-api.hamzie.site/"))

    @discord.ui.button(label="Run the command again!", style=discord.ButtonStyle.primary)
    async def rerun_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://dog.ceo/api/breeds/image/random")
                response.raise_for_status()
                data = response.json()
                image_url = data["message"]
                embed = discord.Embed(
                    color=discord.Colour.blurple()
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
    async def dogs(self, interaction: discord.Interaction):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://dog.ceo/api/breeds/image/random")
                response.raise_for_status()
                data = response.json()
                image_url = data["message"]
                embed = discord.Embed(
                    color=discord.Colour.blurple()
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