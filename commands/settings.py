import discord
from discord.ext import commands
from discord import app_commands
from userLocale import setLang
from userLocale import getLang
import importlib

class SettingsCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    settings = app_commands.Group(name="settings", description="Manage your settings.")

    @settings.command(name="language", description="Set your preferred language.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.choices(locale=[
        app_commands.Choice(name="English (en_US)", value="en_US"),
        app_commands.Choice(name="Dutch (nl_NL)", value="nl_NL"),
        app_commands.Choice(name="Romanian (ro_RO)", value="ro_RO")
    ])
    async def language(self, interaction: discord.Interaction, locale: str):
        setLang(interaction.user.id, locale)
        ### LANG SECTION ###
        user_locale = getLang(interaction.user.id)
        lang_module = f"lang.settings.{user_locale}"
        try:
            lang = importlib.import_module(lang_module)
        except ModuleNotFoundError:
            import lang.settings.en_US as lang
            print(f"[!] Error loading language file. Defaulting to en_US | File not found: {lang_module} | User locale: {user_locale}")
        ### END OF LANG SECTION ###
        await interaction.response.send_message(f"{lang.lang_set} `{locale}`{lang.lang_set2}\n\n{lang.lang_warn}")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(SettingsCog(client))
