import discord
from discord.ext import commands
from discord import app_commands
import config
from i18n import i18n

AVA_VERSION = config.AVA_VERSION

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    # General
    @discord.ui.button(label="General",style=discord.ButtonStyle.primary)
    async def general_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('help', user_locale)

        embed = discord.Embed(
            color=discord.Colour.blurple(),
            title=f"Ava | {lang.general_title}",
            description=lang.general_description)
        embed.add_field(name='/help', value=lang.general_help, inline=False)
        embed.add_field(name='/about', value=lang.general_about, inline=False)
        embed.add_field(name='/embed', value=lang.general_embed, inline=False)
        embed.set_footer(text=f"Ava | {lang.version}: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.defer()
        await interaction.edit_original_response(embed=embed, view=Buttons())

    # Fun
    @discord.ui.button(label="Fun",style=discord.ButtonStyle.primary)
    async def fun_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('help', user_locale)

        embed = discord.Embed(
            color=discord.Colour.blurple(),
            title=f"Ava | {lang.fun_title}",
            description=lang.fun_description)
        embed.add_field(name='/hug', value=lang.fun_hug, inline=False)
        embed.add_field(name='/kiss', value=lang.fun_kiss, inline=False)
        embed.add_field(name='/headpats', value=lang.fun_headpats, inline=False)
        embed.add_field(name='/slap', value=lang.fun_slap, inline=False)
        embed.add_field(name='/cats', value=lang.fun_cats, inline=False)
        embed.add_field(name='/xiaojie', value=lang.fun_xiaojie, inline=False)
        embed.add_field(name='/dogs', value=lang.fun_dogs, inline=False)
        embed.add_field(name='/ball', value=lang.fun_ball, inline=False)
        embed.add_field(name='/trivia', value=lang.fun_trivia, inline=False)
        embed.add_field(name='/typerace', value=lang.fun_typerace, inline=False)
        embed.set_footer(text=f"Ava | {lang.version}: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.defer()
        await interaction.edit_original_response(embed=embed, view=Buttons())

    # Music
    @discord.ui.button(label="Music",style=discord.ButtonStyle.primary)
    async def music_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('help', user_locale)

        embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=f"Ava | {lang.music_title}",
                description=lang.music_description)
        embed.add_field(name=f'/play <{lang.music_query}>', value=lang.music_play, inline=False)
        embed.add_field(name='/nowplaying', value=lang.music_nowplaying, inline=False)
        embed.add_field(name='/skip', value=lang.music_skip, inline=False)
        embed.add_field(name=f'/queue [{lang.music_page}]', value=lang.music_queue, inline=False)
        embed.add_field(name='/leave', value=lang.music_leave, inline=False)
        embed.set_footer(text=f"Ava | {lang.version}: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.defer()
        await interaction.edit_original_response(embed=embed, view=Buttons())
    
    # settings
    @discord.ui.button(label="Settings",style=discord.ButtonStyle.primary)
    async def settings_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('help', user_locale)

        embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=f"Ava | {lang.settings_title}",
                description=lang.settings_description)
        embed.add_field(name=f'/settings language <{lang.settings_language}>', value=lang.settings_lang, inline=False)
        embed.set_footer(text=f"Ava | {lang.version}: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.defer()
        await interaction.edit_original_response(embed=embed, view=Buttons())

class help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="help", description="Information about my commands.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def help(self, interaction: discord.Interaction):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('help', user_locale)

        embed = discord.Embed(
            color=discord.Colour.blurple(),
            title=f"{lang.help_title} <:Ava_CatBlush:1210004576082853939>",
            description=lang.help_description)
        embed.set_footer(text=f"Ava | {lang.version}: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.send_message(embed=embed, view=Buttons())
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.client.user.mentioned_in(message) and not (message.mention_everyone):
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=f"{lang.help_title} <:Ava_CatBlush:1210004576082853939>",
                description=lang.help_description)
            embed.set_footer(text=f"Ava | {lang.version}: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await message.channel.send(embed=embed, view=Buttons())

async def setup(client:commands.Bot) -> None:
    await client.add_cog(help(client))