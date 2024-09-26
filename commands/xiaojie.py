import discord
from discord.ext import commands
from discord import app_commands
import httpx
import config

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    # Rerun button
    @discord.ui.button(label="Run the command again!",style=discord.ButtonStyle.primary)
    async def rerun_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.hamzie.site/v1/images/xiaojie")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title="Xiaojie Cat",
                    description="115 **new** images of Xiaojie have been added! In total, Hamzie API stores 295 images of the cute Xiaojie cat. Have you seen every one?"
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: hamzie.site/api", icon_url=config.FOOTER_ICON)

                await interaction.response.send_message(embed=embed, view=Buttons())
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

class xiaojie(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="xiaojie", description="Get your daily dose of xiaojie cat pictures :)")
    async def xiaojie(self, interaction: discord.Interaction):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.hamzie.site/v1/images/xiaojie")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title="Xiaojie Cat",
                    description="115 **new** images of Xiaojie have been added! In total, Hamzie API stores 295 images of the cute Xiaojie cat. Have you seen every one?"
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: hamzie.site/api", icon_url=config.FOOTER_ICON)

                await interaction.response.send_message(embed=embed, view=Buttons())
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(xiaojie(client))