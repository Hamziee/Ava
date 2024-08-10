import discord
from discord.ext import commands
from discord import app_commands
import time
import config
import httpx

class ping(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="ping", description="Calculate current latency.")
    async def ping(self, interaction: discord.Interaction):
        try:
            start = time.time()
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title='Pinging...',
                description='🤔')
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.response.send_message(embed=embed)
            end = time.time()
            duration = round((end - start) * 100)
            durationtext = f"{duration}ms"
            try:
                startapi = time.time()
                async with httpx.AsyncClient() as client:
                    response = await client.get("https://api.hamzie.site/v1/gifs/hug")
                    response.raise_for_status()
                endapi = time.time()
                durationapi = round((endapi - startapi) * 100)
                durationapitext = f"{durationapi}ms"
            except:
                durationapitext = "No Response"
            embed = discord.Embed(
                title="Pong!", 
                description=f"Discord API & Ava Latency: {durationtext}\nHamzie API Latency: {durationapitext} \n\n**What does this mean?**\nLatency is calculated to measure the responsiveness and performance of the bot and the Discord server. It helps users assess the speed at which the bot can send and receive messages, providing valuable feedback on its operational efficiency. \n\nThis information is crucial for bot developers and users to ensure that the bot is functioning optimally and to identify any potential issues that may affect its performance.", 
                color=discord.Color.blurple())
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(ping(client))