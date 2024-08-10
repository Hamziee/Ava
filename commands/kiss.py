# Thanks to Hamzie API for their unlimited free use of their API.

import discord
from discord.ext import commands
from discord import app_commands
import httpx
from datetime import datetime
import config

class kiss(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="kiss", description="Kiss your friend/lover!")
    @app_commands.rename(member='person')
    async def kiss(self, interaction: discord.Interaction, member: discord.Member):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.hamzie.site/v1/gifs/kiss")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                embed = discord.Embed(
                    color=discord.Colour.blurple()
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: api.hamzie.site", icon_url=config.FOOTER_ICON)
                
                if member.id == interaction.user.id:
                    await interaction.response.send_message(content="You can't kiss yourself! Here I will give you a big kiss! <a:ava_CatCuddle:1244799986600902758>", embed=embed)
                    return
                if member.id == config.BOT_ID:
                    await interaction.response.send_message(content="Here I will give you a big kiss! <a:AVA_hugg:1244799800378130472>", embed=embed)
                    return
                if member.bot:
                    await interaction.response.send_message(content="Bots don't need kisses! But I do, so here is a kiss for you! <a:AVA_cats_hug:1244799755960451159>", embed=embed)
                    return
                await interaction.response.send_message(content= f"{interaction.user.mention} kisses {member.mention} <:AVA_hug:1244799683042344970>", embed=embed)
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(kiss(client))