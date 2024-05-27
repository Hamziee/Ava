import discord
from discord.ext import commands
from discord import app_commands
import httpx
from datetime import datetime
import config

class hug(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="hug", description="Hug your (imaginary) friend/lover!")
    @app_commands.rename(member='person')
    async def hug(self, interaction: discord.Interaction, member: discord.Member):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.hamzie.site/v1/gifs/hug")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                embed = discord.Embed(
                    color=discord.Colour.blurple()
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: api.hamzie.site", icon_url="https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp")

                await interaction.response.send_message(content= f"{interaction.user.mention} hugs {member.mention}", embed=embed)
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(hug(client))