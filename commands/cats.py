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

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

        # Add the submit cat button with a URL
        self.add_item(discord.ui.Button(label="Submit Your Cat!", style=discord.ButtonStyle.link, url="https://upload-api.hamzie.site/"))

    @discord.ui.button(label="Run the command again!", style=discord.ButtonStyle.primary)
    async def rerun_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.thecatapi.com/v1/images/search", headers={"x-api-key": config.THECATAPI_KEY})
                data = response.json()
                image_url = data[0]['url']

            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title="Important Message:",
                description="Currently Ava uses TheCatAPI which is not free to use, that's why Hamzie API (the source of most images Ava uses) is making their own cat's section, free to use for everyone. We ask you to send in your best cat pictures, for it to be used in Hamzie API, which will eventually replace TheCatAPI in this command."
            )
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: thecatapi.com", icon_url=config.FOOTER_ICON)

            await interaction.response.send_message(embed=embed, view=Buttons())
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')


class cats(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="cats", description="Get your daily dose of cats :)")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
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
                color=discord.Colour.blurple(),
                title="Important Message:",
                description="Currently the bot uses TheCatAPI which is not free to use, that's why Hamzie API (the source of most images Ava uses) is making their own cat's section, free to use for everyone. We ask you to send in your best cat pictures, for it to be used in Hamzie API, which will eventually replace TheCatAPI in this command."
            )
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: thecatapi.com", icon_url=config.FOOTER_ICON)

            await interaction.response.send_message(embed=embed, view=Buttons())
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(cats(client))