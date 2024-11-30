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
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def headpats(self, interaction: discord.Interaction, member: discord.User):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.hamzie.site/v1/gifs/headpats")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                desctxt = f"{interaction.user.mention} gives head pats to {member.mention}"
                if member.id == interaction.user.id:
                        desctxt = "You can't give head pats to yourself! But here, let me give you some head pats! <:AVA_headpat:1245509705703362560>"
                if member.id == config.BOT_ID:
                        desctxt = "Here, let me give you some head pats! <:AVA_headpat:1245509705703362560>"
                if member.bot:
                        desctxt = "Bots don't need head pats! But you do, so here are some headpats for you! <:AVA_headpat:1245509705703362560>"
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
    await client.add_cog(headpats(client))