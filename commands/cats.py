import discord
from discord.ext import commands
from discord import app_commands
import requests
from datetime import datetime
import random

class cats(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="cats", description="Get your daily dose of pictures and gifs of cats :)")
    async def cats(self, interaction: discord.Interaction):
        try:
            now = datetime.now()
            timestamp = round(datetime.timestamp(now))
            response = requests.get(f"https://cataas.com/cat?timestamp={timestamp}")
            image_url = response.url

            embed = discord.Embed(
                color=discord.Colour.blurple(),
                #title='Random Cat Image',
                #description='Here is a random image of a cat:'
            )
            embed.set_image(url=image_url)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(cats(client))