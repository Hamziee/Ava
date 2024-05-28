import discord
from discord.ext import commands
from discord import app_commands
import httpx
from datetime import datetime
import config

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
                    color=discord.Colour.blurple()
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: api.hamzie.site", icon_url=config.FOOTER_ICON)

                await interaction.response.send_message(embed=embed)
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(xiaojie(client))