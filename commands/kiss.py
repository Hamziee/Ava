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
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def kiss(self, interaction: discord.Interaction, member: discord.User):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.hamzie.site/v1/gifs/kiss")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                desctxt = f"{interaction.user.mention} kisses {member.mention} <:AVA_hug:1244799683042344970>"
                if member.id == interaction.user.id:
                    desctxt="You can't kiss yourself! Here I will give you a big kiss! <a:ava_CatCuddle:1244799986600902758>"
                if member.id == config.BOT_ID:
                    desctxt="Here I will give you a big kiss! <a:AVA_hugg:1244799800378130472>"
                if member.bot:
                    desctxt="Bots don't need kisses! But I do, so here is a kiss for you! <a:AVA_cats_hug:1244799755960451159>"
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    description=desctxt
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: hamzie.site/api", icon_url=config.FOOTER_ICON)
                await interaction.response.send_message(embed=embed)
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(kiss(client))