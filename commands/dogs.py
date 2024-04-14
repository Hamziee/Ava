import discord
from discord.ext import commands
from discord import app_commands
import httpx
from datetime import datetime

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

                await interaction.response.send_message(embed=embed)
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(dogs(client))