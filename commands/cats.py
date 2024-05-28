import discord
from discord.ext import commands
from discord import app_commands
from colorama import Back, Fore, Style
import httpx
from datetime import datetime
import config
global cats_enabled
if config.THECATAPI_KEY == 'your thecatapi key here':
    print(Fore.RED + Style.BRIGHT + "Please provide your thecatapi key in config.py.\nThe cats command will not work without it.\nGet your own free key at https://thecatapi.com/\n\nIf you wish to hide this error, please put cats.py in the disabled_commands folder." + Fore.RESET)
    cats_enabled = False
else:
    cats_enabled = True

class cats(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="cats", description="Get your daily dose of cats :)")
    async def cats(self, interaction: discord.Interaction):
        if cats_enabled == False:
            print(Fore.RED + Style.BRIGHT + "[!] User tried to run cats command.\nPlease provide your thecatapi key in config.py.\nThe cats command will not work without it.\nGet your own free key at https://thecatapi.com/\n\nIf you wish to hide this error, please put cats.py in the disabled_commands folder." + Fore.RESET)
            await interaction.response.send_message(content='The cats command is disabled due to missing thecatapi key. Please contact the bot owner.\n\nNote for bot owner: If you wish to hide this error, please put cats.py in the disabled_commands folder.')
            return
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.thecatapi.com/v1/images/search", headers={"x-api-key": config.THECATAPI_KEY})
                data = response.json()
                image_url = data[0]['url']

            embed = discord.Embed(
                color=discord.Colour.blurple()
            )
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: thecatapi.com", icon_url=config.FOOTER_ICON)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(cats(client))