import discord
from discord.ext import commands
from discord import app_commands
import httpx
from datetime import datetime
import config

class headpats(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="headpats", description="Give headpats to your friend/lover!")
    @app_commands.rename(member='person')
    async def headpats(self, interaction: discord.Interaction, member: discord.Member):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.hamzie.site/v1/gifs/headpats")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                embed = discord.Embed(
                    color=discord.Colour.blurple()
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | version: {config.AVA_VERSION} - Image by: hamzie.site/api", icon_url=config.FOOTER_ICON)
                
                if member.id == interaction.user.id:
                    await interaction.response.send_message(content="You can't give head pats to yourself! But here, let me give you some head pats! <:AVA_headpat:1245509705703362560>", embed=embed)
                    return
                if member.id == config.BOT_ID:
                    await interaction.response.send_message(content="Here, let me give you some head pats! <:AVA_headpat:1245509705703362560>", embed=embed)
                    return
                if member.bot:
                    await interaction.response.send_message(content="Bots don't need head pats! But I do, so here are some headpats for you! <:AVA_headpat:1245509705703362560>", embed=embed)
                    return
                await interaction.response.send_message(content= f"{interaction.user.mention} gives head pats to {member.mention} <:AVA_headpat:1245509705703362560>", embed=embed)
        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(headpats(client))