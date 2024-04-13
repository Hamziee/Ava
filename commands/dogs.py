import discord
from discord.ext import commands
from discord import app_commands
import requests
from datetime import datetime

class dogs(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="dogs", description="Get your daily dose of dogs :)")
    async def dogs(self, interaction: discord.Interaction):
        try:
            response = requests.get("https://dog.ceo/api/breeds/image/random")
            if response.status_code == 200:
                data = response.json()
                image_url = data["message"]
                embed = discord.Embed(
                    color=discord.Colour.blurple()
                )
                embed.set_image(url=image_url)

                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(content='Failed to fetch dog image')
                raise Exception("Failed to fetch dog image")

        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(dogs(client))