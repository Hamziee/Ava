
# IMPORTANT NOTE:
# AvaAI is closed source for now. ChatAI will NOT work for you unless you make your function for this command to process! If you do not know what that means then don't bother getting this to work, I might add an example script to use OpenAI in the future.
# This script calls for ChatReponse() to respond with a message.


# This is in progress of begin rewritten

import discord
from discord.ext import commands
from discord import app_commands
import config
from extraConfigs.ChatAIConfig import *

class chat(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="chat", description="Chat with me!")
    @app_commands.rename(message='message')
    @app_commands.describe(message='Type the message you wish to send to Ava.')
    async def chat(self, interaction: discord.Interaction, message: str):
        try:
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title="AvaAI 💬",
                description="Ava is thinking... <:AVA_CuteThink:1211038099086512199>")
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} | Keep in mind that Ava can make mistakes.", icon_url=config.FOOTER_ICON)
            await interaction.response.send_message(embed=embed)
            response = await ChatReponse(message)
            try:
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title="AvaAI 💬",
                    description=response)
                embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} | Keep in mind that Ava can make mistakes.", icon_url=config.FOOTER_ICON)
                await interaction.edit_original_response(embed=embed)
            except:
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title="AvaAI <:Ava_Error:1211046596373123174>",
                    description="Ava's response overwhelmed Discord with its size. Could you please ask her to provide a shorter response?")
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} | Keep in mind that Ava can make mistakes.", icon_url=config.FOOTER_ICON)
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(chat(client))
