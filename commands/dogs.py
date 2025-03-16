import discord
from discord.ext import commands
from discord import app_commands
import config
import httpx
from i18n import i18n

class dogs(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="dogs", description="Get your daily dose of dog pictures!")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def dogs(self, interaction: discord.Interaction):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('dogs', user_locale)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://dog.ceo/api/breeds/image/random")
                response.raise_for_status()
                data = response.json()

            if data and "message" in data:
                image_url = data["message"]

                embed = discord.Embed(color=discord.Colour.blurple(), title=lang.title)
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION} | {lang.by}: dog.ceo", icon_url=config.FOOTER_ICON)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(content=lang.error)
        except Exception as e:
            print(e)
            await interaction.followup.send(content=lang.error)

async def setup(client: commands.Bot):
    await client.add_cog(dogs(client))