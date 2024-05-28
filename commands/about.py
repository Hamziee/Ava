import discord
from discord.ext import commands
from discord import app_commands
import config

class about(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="about", description="Some information about me!")
    async def about(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title="Hi I'm Ava! <:Ava_CatBlush:1210004576082853939>",
                description="I am an versatile and open-source Discord bot designed to serve all your needs effortlessly. With Ava by your side, managing your server becomes a breeze. From moderation tools to fun utilities, Ava has it all covered. Embrace simplicity and functionality with Ava, the reliable companion for any Discord community.\n### [Request Feature](https://github.com/Hamziee/Ava/issues/new) **|** [Github](https://github.com/Hamziee/Ava>) **|** [Maintainer](<https://github.com/Hamziee/>) \n[Hosted by HEO Systems](<https://heo-systems.net>)\n\n**Developer Note:** Ava is currently a work in progress, and I am working on adding new and exciting features to Ava. Please bear in mind that this is a project of mine that I work on in my free time, so don't expect fast progress. - Hamza")
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(about(client))
