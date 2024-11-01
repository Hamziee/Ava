import discord
from discord.ext import commands
from discord import app_commands
import config
import sys
import requests
from importlib.metadata import distributions

class info(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="technical_information", description="Display technical information")
    async def info(self, interaction: discord.Interaction):
        try:
            # Version Checker
            url = "https://cdn.hamzie.site/Ava/VRC/core.txt"
            response = requests.get(url)
            remote_version = response.text.strip() if response.status_code == 200 else "Failed to fetch."

            # TheCatAPI Check
            cats_string = 'Enabled' if config.THECATAPI_KEY != 'your thecatapi key here' else 'Disabled'

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
                title="Technical Details",
                description="If you are looking for information about the bot, run the command: '/about'")
            embed.add_field(name='Core', value=f'Running Ava {config.AVA_VERSION} | (Latest: {remote_version})\nAva Config Version: {config.CONFIG_VERSION}\nPython {python_version}', inline=False)
            embed.add_field(name="Python Packages", value=package_string, inline=False)
            AvaAIver = "Disabled"
            try:
                import commands.AvaAI as AvaAI
                AvaAIver = AvaAI.AvaAIver
            except:
                pass
            embed.add_field(name="Ava Optional Modules", value=f'AvaAI: {AvaAIver} - In Development | (Being Rewritten)\nTheCatAPI: {cats_string} | (Will be removed in the future in favor of a new system that will be provided by Hamzie API)', inline=False)
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occurred.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(info(client))
