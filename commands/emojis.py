import discord
from discord.ext import commands
from discord import app_commands
import config
AVA_VERSION = config.AVA_VERSION

class emojis(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="emojis", description="See a list of emojis you can add to your server.")
    @app_commands.choices(category=[
        discord.app_commands.Choice(name='Cats', value=1)
    ])
    async def embed(self, interaction: discord.Interaction, category: discord.app_commands.Choice[int]):
        
        if category.name == 'Cats':	
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title="Ava | My Cats Emojis <:Ava_CatBlush:1210004576082853939>",
                description="Here is a list of emojis you can add to your server. With the command /addemoji <emoji-name> you can add them to your server. (Coming Soon)")
            embed.add_field(name='', value='<:Ava_CatBlush:1210004576082853939> <a:CatCry:1233560699108851773> <a:CatSpin:1233560664912564306> <a:NecoArcTailWag:1233560749817856000> <a:ava_CatCuddle:1233561059697365124> <a:ava_CatHug:1233561040130801746> <:ava_CatScream:1233560577583087668> <a:ava_CatSleepy:1233560899873144903> <a:ava_Popcat_eat_popcorn:1233561161899966539> <:ava_Puke_Cat:1233560945608101919> <:ava_WHATDAHELL:1233560973671923755> <a:ava_catStuck:1233561080014307338><:ava_chinesecatstare:1233561195554930769> <a:ava_hubert:1233560921646039150> <a:newspaper_cat:1233560725230714960>', inline=False)
            embed.add_field(name='', value='You will soon be able to join or add your own bot to use these emojis.', inline=False)
            embed.set_footer(text=f"Ava | version: {AVA_VERSION}", icon_url="https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.followup.send(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(emojis(client))