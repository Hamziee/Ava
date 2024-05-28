import discord
from discord.ext import commands
from discord import app_commands
import config
PREFIX = config.PREFIX
AVA_VERSION = config.AVA_VERSION

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    
    # General
    @discord.ui.button(label="General",style=discord.ButtonStyle.primary)
    async def general_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            color=discord.Colour.blurple(),
            title="Ava | General Commands",
            description="Here is some information about my commands :)")
        embed.add_field(name='/help', value='Shows up this.', inline=False)
        embed.add_field(name='/about', value='Some information about me!', inline=False)
        embed.add_field(name='/embed', value='Make an embed message.', inline=False)
        embed.add_field(name='/chat', value='Chat with my AI!', inline=False)
        embed.set_footer(text=f"Ava | version: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.defer()
        await interaction.edit_original_response(embed=embed, view=Buttons())

    # Fun
    @discord.ui.button(label="Fun",style=discord.ButtonStyle.primary)
    async def fun_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            color=discord.Colour.blurple(),
            title="Ava | Enjoyable Commands",
            description="Here is some information about my commands :)")
        embed.add_field(name='/chat', value='Chat with my AI!', inline=False)
        embed.add_field(name='/cats', value='Get your daily dose of cat pictures!', inline=False)
        embed.add_field(name='/xiaojie', value='Get your daily dose of xiaojie cat pictures!', inline=False)
        embed.add_field(name='/dogs', value='Get your daily dose of dog pictures!', inline=False)
        embed.set_footer(text=f"Ava | version: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.defer()
        await interaction.edit_original_response(embed=embed, view=Buttons())

    # Music
    @discord.ui.button(label="Music",style=discord.ButtonStyle.primary)
    async def music_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
                color=discord.Colour.blurple(),
                title="Music | Music Commands",
                description="Here is some Information about my music commands :)")
        embed.add_field(name=f'{PREFIX}leave, {PREFIX}l, {PREFIX}disconnect', value='Clears the queue and leaves the voice channel.', inline=False)
        embed.add_field(name=f'{PREFIX}now, {PREFIX}current, {PREFIX}playing', value='Displays the currently playing song.', inline=False)
        embed.add_field(name=f'{PREFIX}pause, {PREFIX}pa', value='Pauses the currently playing song.', inline=False)
        embed.add_field(name=f'{PREFIX}resume, {PREFIX}r', value='Resumes a currently paused song.', inline=False)
        embed.add_field(name=f'{PREFIX}stop, {PREFIX}st, {PREFIX}close', value='Stops playing song and clears the queue.', inline=False)
        embed.add_field(name=f'{PREFIX}skip, {PREFIX}s, {PREFIX}sk', value='Vote to skip a song. The requester can automatically skip.', inline=False)
        embed.add_field(name=f'{PREFIX}queue, {PREFIX}q', value='Shows the queue. You can optionally specify the page to show. Each page contains 10 songs.', inline=False)
        embed.add_field(name=f'{PREFIX}remove', value='Removes a song from the queue at a given index.', inline=False)
        embed.add_field(name=f'{PREFIX}play, {PREFIX}p', value='Plays a song.', inline=False)
        embed.set_footer(text=f"Ava | version: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.defer()
        await interaction.edit_original_response(embed=embed, view=Buttons())

class help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="help", description="Information about my commands.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            color=discord.Colour.blurple(),
            title="Hi I'm Ava! <:Ava_CatBlush:1210004576082853939>",
            description="Choose a category below.")
        embed.set_footer(text=f"Ava | version: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.send_message(embed=embed, view=Buttons())
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.client.user.mentioned_in(message) and not (message.mention_everyone):
            embed = discord.Embed(
            color=discord.Colour.blurple(),
            title="Hi I'm Ava! <:Ava_CatBlush:1210004576082853939>",
            description="Choose a category below.")
            embed.set_footer(text=f"Ava | version: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await message.channel.send(embed=embed, view=Buttons())


async def setup(client:commands.Bot) -> None:
    await client.add_cog(help(client))