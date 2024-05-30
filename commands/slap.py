import discord
from discord.ext import commands
from discord import app_commands
import httpx
from datetime import datetime
import config

class Slap(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="slap", description="Slap your friend/lover!")
    @app_commands.rename(member='person')
    async def slap(self, interaction: discord.Interaction, member: discord.Member):
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
                    embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: api.hamzie.site", icon_url=config.FOOTER_ICON)
                    await interaction.response.send_message(content="You don't need to slap yourself! How about a hug instead?", embed=embed)
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
                    embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: api.hamzie.site", icon_url=config.FOOTER_ICON)
                    await interaction.response.send_message(content="Hey, you can't slap me! But it's okay, here's a hug for you.", embed=embed)
                    return
                response = await client.get("https://api.hamzie.site/v1/gifs/slap")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                embed = discord.Embed(
                    color=discord.Colour.blurple()
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: api.hamzie.site", icon_url=config.FOOTER_ICON)
                await interaction.response.send_message(content=f"{interaction.user.mention} slaps {member.mention}", embed=embed)
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Slap(client))
