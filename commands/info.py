import discord
from discord.ext import commands
from discord import app_commands
import config
import sys
import pkg_resources
import requests

class info(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="technical_information", description="Display technical information")
    async def info(self, interaction: discord.Interaction):
        try:
            # Version Checker
            # Get the content from the URL
            url = "https://cdn.hamzie.site/Ava/VRC/core.txt"
            response = requests.get(url)

            # Check if the content matches the AVA_VERSION
            if response.status_code == 200:  # Make sure the request was successful
                remote_version = response.text.strip()
            else:
                remote_version = "Failed to fetch."

            # TheCatAPI Check
            if config.THECATAPI_KEY == 'your thecatapi key here':
                cats_string = 'Disabled'
            else:
                cats_string = 'Enabled'
            
            # Python Version
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

            # Get installed packages and format them
            installed_packages = pkg_resources.working_set
            package_list = "\n".join([f"{package.project_name} {package.version}" for package in installed_packages])
            
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title="Technical Details",
                description="If you are looking for information about the bot, run the command: '/about'")
            embed.add_field(name='Core', value=f'Running Ava {config.AVA_VERSION} | (Latest: {remote_version})\nAva Config Version: {config.CONFIG_VERSION}\nPython {python_version}', inline=False)
            embed.add_field(name="Python Packages", value=package_list, inline=False)
            embed.add_field(name="Ava Optional Modules", value=f'AvaAI: Disabled - In Development | (Being Rewritten)\nTheCatAPI: {cats_string} | (Will be removed in favor of a new system that will be provided by Hamzie API)', inline=False)
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(info(client))