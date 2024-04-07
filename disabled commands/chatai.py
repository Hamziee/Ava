
# IMPORTANT NOTE:
# AvaAI is closed source for now. ChatAI will NOT work for you unless you make your function for this command to process! If you do not know what that means then don't bother getting this to work, I might add an example script to use OpenAI in the future.
# This script calls for ChatReponse() to respond with a message.

import discord
from discord.ext import commands
from discord import app_commands
import config
from AvaAI import *

class chat(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="chat", description="Chat with me!")
    @app_commands.rename(message='message')
    @app_commands.describe(message='Type the message you wish to send to Mia.')
    async def chat(self, interaction: discord.Interaction, message: str):
        try:
            if interaction.user.id == config.OWNER_ID:
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title="MiaAI DEV 💬",
                    description="Mia is thinking... <:MIA_CuteThink:1211038099086512199>")
                embed.set_footer(text=f"Mia | version: DEV {config.MIA_VERSION} | Keep in mind that Mia can make mistakes.", icon_url="https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp")
                await interaction.response.send_message(embed=embed)
                response = await ChatReponseHamza(message)
                try:
                    embed = discord.Embed(
                        color=discord.Colour.blurple(),
                        title="MiaAI DEV 💬",
                        description=response)
                    embed.set_footer(text=f"Mia | version: DEV {config.MIA_VERSION} | Keep in mind that Mia can make mistakes.", icon_url="https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp")
                    await interaction.edit_original_response(embed=embed)
                except:
                    embed = discord.Embed(
                        color=discord.Colour.blurple(),
                        title="MiaAI DEV <:MIA_Error:1211046596373123174>",
                        description="Mia's response overwhelmed Discord with its size. Could you please ask her to provide a shorter response?")
                embed.set_footer(text=f"Mia | version: DEV {config.MIA_VERSION} | Keep in mind that Mia can make mistakes.", icon_url="https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp")
                await interaction.edit_original_response(embed=embed)
            else:
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title="MiaAI 💬",
                    description="Mia is thinking... <:MIA_CuteThink:1211038099086512199>")
                embed.set_footer(text=f"Mia | version: {config.MIA_VERSION} | Keep in mind that Mia can make mistakes.", icon_url="https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp")
                await interaction.response.send_message(embed=embed)
                response = await ChatReponse(message)
                try:
                    embed = discord.Embed(
                        color=discord.Colour.blurple(),
                        title="MiaAI 💬",
                        description=response)
                    embed.set_footer(text=f"Mia | version: {config.MIA_VERSION} | Keep in mind that Mia can make mistakes.", icon_url="https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp")
                    await interaction.edit_original_response(embed=embed)
                except:
                    embed = discord.Embed(
                        color=discord.Colour.blurple(),
                        title="MiaAI <:MIA_Error:1211046596373123174>",
                        description="Mia's response overwhelmed Discord with its size. Could you please ask her to provide a shorter response?")
                embed.set_footer(text=f"Mia | version: {config.MIA_VERSION} | Keep in mind that Mia can make mistakes.", icon_url="https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp")
                await interaction.edit_original_response(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(chat(client))
