import discord
from discord.ext import commands
from discord import app_commands
import time

class ping(commands.Cog):
  def __init__(self, client: commands.Bot):
    self.client = client

  @app_commands.command(name="ping", description="Ping Pong or something")
  async def ping(self, interaction: discord.Interaction):
    try:
      start = time.time()
      embed = discord.Embed(
          color=discord.Colour.blurple(),
          title='Pinging...',
          description='🤔')
      await interaction.response.send_message(embed=embed)
      end = time.time()
      duration = round((end - start) * 1000)
      embed = discord.Embed(
          title="Pong!", 
          description=f"Latency: {duration}ms. \n\n**What does this mean?**\n Latency is calculated to measure the responsiveness and performance of the bot and the Discord server. It helps users assess the speed at which the bot can send and receive messages, providing valuable feedback on its operational efficiency. \n\nThis information is crucial for bot developers and users to ensure that the bot is functioning optimally and to identify any potential issues that may affect its performance.", 
          color=discord.Color.blurple())
      await interaction.edit_original_response(embed=embed)
    except Exception as e:
      print(e)
      await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
  await client.add_cog(ping(client))