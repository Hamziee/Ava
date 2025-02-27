import discord
from discord.ext import commands
from discord import app_commands
import config
from userLocale import getLang
import importlib

class about(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="about", description="Some information about me!")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def about(self, interaction: discord.Interaction):
        ### LANG SECTION ###
        user_locale = getLang(interaction.user.id)
        lang_module = f"lang.about.{user_locale}"
        try:
            lang = importlib.import_module(lang_module)
        except ModuleNotFoundError:
            import lang.cats.en_US as lang
            print(f"[!] Error loading language file. Defaulting to en_US | File not found: {lang_module} | User locale: {user_locale}")
        ### END OF LANG SECTION ###
        
        try:
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=lang.title,
                description=lang.description)
            embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(about(client))
