import discord
from discord.ext import commands
from discord import app_commands
import config
prefix = config.PREFIX
MIA_VERSION = config.MIA_VERSION


class help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="help", description="Information about my commands.")
    @app_commands.rename(category='category')
    @app_commands.describe(category='Specify a category of the help command. (general, music)')
    async def help(self, interaction: discord.Interaction, category: str):
        if category == 'music'.lower():
            try:
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title="Hi I'm Mia! <:MIA_CatBlush:1210004576082853939>",
                    description="Here is some Information about my music commands :)")
                embed.add_field(name='Music', value=
                                f"""**{prefix}leave, {prefix}l, {prefix}disconnect** - Clears the queue and leaves the voice channel.
                                **{prefix}now, {prefix}current, {prefix}playing** - Displays the currently playing song.
                                **{prefix}pause, {prefix}pa** - Pauses the currently playing song.
                                **{prefix}resume, {prefix}r** - Resumes a currently paused song.
                                **{prefix}stop, {prefix}st, {prefix}close** - Stops playing song and clears the queue.
                                **{prefix}skip, {prefix}s, {prefix}sk** - Vote to skip a song. The requester can automatically skip.
                                **{prefix}queue, {prefix}q** - Shows the player's queue. You can optionally specify the page to show. Each page contains 10 songs.
                                **{prefix}remove** - Removes a song from the queue at a given index.
                                **{prefix}play, {prefix}p** - Plays a song.""", inline=False)
                embed.add_field(name='Other commands', value=
                                f""" Run **/help** for all the other commands.""", inline=False)
                embed.set_footer(text=f"Mia | version: {MIA_VERSION}", icon_url="https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp")
                await interaction.response.send_message(embed=embed)
            except Exception as e:
                print(e)
                await interaction.followup.send(content='Error occured.')
        else:
            try:
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    title="Hi I'm Mia! <:MIA_CatBlush:1210004576082853939>",
                    description="Here is some information about my commands :)")
                embed.add_field(name='General', value=
                                f"""**/help** - Shows up this.
                                **/about** - Some information about me!
                                **/chat** - Chat with my AI!""", inline=False)
                embed.add_field(name='Music commands', value=
                                f""" Run **/help music** for information about all my music commands.""", inline=False)
                embed.set_footer(text=f"Mia | version: {MIA_VERSION}", icon_url="https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp")
                await interaction.response.send_message(embed=embed)
            except Exception as e:
                print(e)
                await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(help(client))