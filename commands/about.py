import discord
from discord.ext import commands
from discord import app_commands
import config
import credits
from i18n import i18n

class about(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="about", description="Some information about me!")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def about(self, interaction: discord.Interaction):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('about', user_locale)
        
        try:
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=lang.title,
                description=lang.description)
            embed.add_field(name=f":flag_nl: {lang.lang_nltrans}", value=credits.lang_nl, inline=True)
            embed.add_field(name=f":flag_ro: {lang.lang_rotrans}", value=credits.lang_ro, inline=True)
            embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occurred.')

async def setup(client: commands.Bot):
    await client.add_cog(about(client))
