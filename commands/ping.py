import discord
from discord.ext import commands
from discord import app_commands
import time
import config
import httpx
from i18n import i18n

class ping(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="ping", description="Calculate current latency.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ping(self, interaction: discord.Interaction):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('ping', user_locale)

        try:
            start = time.time()
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=lang.pinging,
                description='🤔')
            await interaction.response.send_message(embed=embed)
            end = time.time()
            duration = round((end - start) * 100)
            durationtext = f"{duration}ms"
            try:
                startapi = time.time()
                async with httpx.AsyncClient() as client:
                    response = await client.get("https://api.hamzie.site/v1/images/xiaojie")
                    response.raise_for_status()
                endapi = time.time()
                durationapi = round((endapi - startapi) * 100)
                durationapitext = f"{durationapi}ms"
            except:
                durationapitext = lang.noresponse
            embed = discord.Embed(
                title=lang.pong, 
                description=f"{lang.discordapi}: {durationtext}\n{lang.hamzieapi}: {durationapitext} \n\n{lang.whatmean}", 
                color=discord.Color.blurple())
            embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content=lang.error)

async def setup(client: commands.Bot):
    await client.add_cog(ping(client))