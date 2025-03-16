import discord
from discord.ext import commands
from discord import app_commands
import config
import sys
import requests
from importlib.metadata import distributions
from i18n import i18n

class info(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="technical_information", description="Display technical information")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def info(self, interaction: discord.Interaction):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('info', user_locale)

        try:
            # Version Checker
            url = "https://cdn.hamzie.site/Ava/VRC/core.txt"
            response = requests.get(url)
            remote_version = response.text.strip() if response.status_code == 200 else lang.failedFetch

            # TheCatAPI Check
            cats_string = lang.enabled if config.THECATAPI_KEY != 'your thecatapi key here' else lang.disabled

            # Python Version
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

            # Get installed packages and format them as a comma-separated list
            package_list = [f"{dist.metadata['Name']} {dist.metadata['Version']}" for dist in distributions()]
            package_string = ", ".join(package_list)

            # Truncate the package string if it's too long
            if len(package_string) > 1024:
                package_string = package_string[:1021] + "..."

            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=lang.title,
                description=lang.description)
            embed.add_field(
                name=lang.core, 
                value=f'{lang.running} Ava {config.AVA_VERSION} | ({lang.latest}: {remote_version})\nAva {lang.cnf_version}: {config.CONFIG_VERSION}\nPython {python_version}', 
                inline=False
            )
            embed.add_field(
                name=lang.py_packages, 
                value=package_string, 
                inline=False
            )
            embed.add_field(
                name=f"Ava {lang.optional_mods}", 
                value=f'TheCatAPI: {cats_string} | ({lang.new_system})', 
                inline=False
            )
            embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            print(e)
            await interaction.followup.send(content=lang.error)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(info(client))
