import discord
from discord.ext import commands
from discord import app_commands
from i18n import i18n

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
        # Set the new locale
        i18n.set_locale(interaction.user.id, locale)
        
        # Get user's current locale for the response
        user_locale = i18n.get_locale(interaction.user.id)
        
        # Get all translations for the settings module
        lang = i18n.get_module('settings', user_locale)
        
        # Now we can use the translations directly like before
        await interaction.response.send_message(f"{lang.lang_set} `{locale}`{lang.lang_set2}\n\n{lang.lang_warn}")

async def setup(client: commands.Bot):
    await client.add_cog(SettingsCog(client))
