import discord
from discord.ext import commands
from discord import app_commands
from colorama import Back, Fore, Style
import httpx
import config
from userLocale import getLang
import importlib
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
        ### LANG SECTION ###
        user_locale = getLang(interaction.user.id)
        lang_module = f"lang.cats.{user_locale}"
        try:
            lang = importlib.import_module(lang_module)
        except ModuleNotFoundError:
            import lang.cats.en_US as lang
            print(f"[!] Error loading language file. Defaulting to en_US | File not found: {lang_module} | User locale: {user_locale}")
        ### END OF LANG SECTION ###
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.thecatapi.com/v1/images/search", headers={"x-api-key": config.THECATAPI_KEY})
                data = response.json()
                image_url = data[0]['url']

            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=lang.title,
                description=lang.description
            )
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION} - {lang.by}: thecatapi.com", icon_url=config.FOOTER_ICON)

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
            await interaction.response.send_message(content=lang.noapikey)
            return
        ### LANG SECTION ###
        user_locale = getLang(interaction.user.id)
        lang_module = f"lang.cats.{user_locale}"
        try:
            lang = importlib.import_module(lang_module)
        except ModuleNotFoundError:
            import lang.cats.en_US as lang
            print(f"[!] Error loading language file. Defaulting to en_US | File not found: {lang_module} | User locale: {user_locale}")
        ### END OF LANG SECTION ###
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.thecatapi.com/v1/images/search", headers={"x-api-key": config.THECATAPI_KEY})
                data = response.json()
                image_url = data[0]['url']

            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=lang.title,
                description=lang.description
            )
            embed.set_image(url=image_url)
            embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION} - {lang.by}: thecatapi.com", icon_url=config.FOOTER_ICON)

            await interaction.response.send_message(embed=embed, view=Buttons())
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(cats(client))