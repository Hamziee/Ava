import discord
from discord.ext import commands
from discord import app_commands
import config
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
        embed.add_field(name='/groupchat', value='Chat with my AI, using the context of the channel!', inline=False)
        embed.add_field(name='/hug', value='Hug your friend/lover!', inline=False)
        embed.add_field(name='/kiss', value='Kiss your friend/lover!', inline=False)
        embed.add_field(name='/headpats', value='Give headpats to your friend/lover!', inline=False)
        embed.add_field(name='/slap', value='Slap someone who deserves it!', inline=False)
        embed.add_field(name='/cats', value='Get your daily dose of cat pictures!', inline=False)
        embed.add_field(name='/xiaojie', value='Get your daily dose of xiaojie cat pictures!', inline=False)
        embed.add_field(name='/dogs', value='Get your daily dose of dog pictures!', inline=False)
        embed.add_field(name='/ball', value='Get the truth of your world breaking question.', inline=False)
        embed.add_field(name='/trivia', value='Test your knowledge with a trivia question!', inline=False)
        embed.add_field(name='/typerace', value='Test your typing skills in a type race!', inline=False)
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
        embed.add_field(name='/play <query>', value='Play a song or add it to the queue.', inline=False)
        embed.add_field(name='/nowplaying', value='See what’s currently playing.', inline=False)
        embed.add_field(name='/skip', value='Skip the current song.', inline=False)
        embed.add_field(name='/queue [page]', value='View the current song queue. (Page is optional.)', inline=False)
        embed.add_field(name='/leave', value='Leave the voice channel and clear the queue.', inline=False)
        embed.set_footer(text=f"Ava | version: {AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.defer()
        await interaction.edit_original_response(embed=embed, view=Buttons())

class help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="help", description="Information about my commands.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
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