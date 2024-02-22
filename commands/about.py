import discord
from discord.ext import commands
from discord import app_commands

class about(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="about", description="Some information about me!")
    async def about(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title="Hi I'm Mia! <:CatBlush:1210004576082853939>",
                description="I am an versatile and open-source Discord bot designed to serve all your needs effortlessly. With Mia by your side, managing your server becomes a breeze. From moderation tools to fun utilities, Mia has it all covered. Embrace simplicity and functionality with Mia, the reliable companion for any Discord community.\n### [Github](<https://github.com/Hamziee/Mia/tree/main>) **|** [Hosted by HEO Systems](<https://heo-systems.net>)\n\n**Developer Note:** Mia is currently a work in progress, and I am working on adding new and exciting features to Mia. Please bear in mind that this is a project of mine that I work on in my free time, so don't expect fast progress. - Hamza")
            embed.set_footer(text="Mia | version: Public Beta 1", icon_url="https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(about(client))