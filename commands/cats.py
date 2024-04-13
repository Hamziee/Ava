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
    @app_commands.choices(choice=[
        discord.app_commands.Choice(name='Random', value=2),
        discord.app_commands.Choice(name='Picture', value=3),
        discord.app_commands.Choice(name='Gif', value=4)])
    async def cats(self, interaction: discord.Interaction, choice: discord.app_commands.Choice[int]):
        try:
            now = datetime.now()
            timestamp = round(datetime.timestamp(now))
            if choice.name == 'Random':
                if random.choice([True, False]):
                    response = requests.get(f"https://cataas.com/cat?timestamp={timestamp}")
                else:
                    response = requests.get(f"https://cataas.com/cat/gif?timestamp={timestamp}")
            elif choice.name == 'Gif':
                response = requests.get(f"https://cataas.com/cat/gif?timestamp={timestamp}")
            elif choice.name == 'Picture':
                response = requests.get(f"https://cataas.com/cat?timestamp={timestamp}")
            else:
                await interaction.response.send_message(content='Invalid choice.')
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