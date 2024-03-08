import discord
from discord.ext import commands
from discord import app_commands
import config

class embed(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="embed", description="Send an embed message.")
    @app_commands.rename(title='title')
    @app_commands.describe(title='Specify the title of the embed.')
    @app_commands.rename(description='description')
    @app_commands.describe(description='Specify the description of the embed.')
    @app_commands.choices(color=[
        discord.app_commands.Choice(name='Aqua', value=2),
        discord.app_commands.Choice(name='Dark Aqua', value=3),
        discord.app_commands.Choice(name='Green', value=4),
        discord.app_commands.Choice(name='Dark Green', value=5),
        discord.app_commands.Choice(name='Blue', value=6),
        discord.app_commands.Choice(name='Dark Blue', value=7),
        discord.app_commands.Choice(name='Purple', value=8),
        discord.app_commands.Choice(name='Dark Purple', value=9),
        discord.app_commands.Choice(name='Luminous Vivid Pink', value=10),
        discord.app_commands.Choice(name='Dark Vivid Pink', value=11),
        discord.app_commands.Choice(name='Gold', value=12),
        discord.app_commands.Choice(name='Dark Gold', value=13),
        discord.app_commands.Choice(name='Orange', value=14),
        discord.app_commands.Choice(name='Dark Orange', value=15),
        discord.app_commands.Choice(name='Red', value=16),
        discord.app_commands.Choice(name='Dark Red', value=17),
        discord.app_commands.Choice(name='Grey', value=18),
        discord.app_commands.Choice(name='Greyple', value=1),
        discord.app_commands.Choice(name='Dark Grey', value=19),
        discord.app_commands.Choice(name='Darker Grey', value=20),
        discord.app_commands.Choice(name='Light Grey', value=21),
        discord.app_commands.Choice(name='Navy', value=22),
        discord.app_commands.Choice(name='Dark Navy', value=23),
        discord.app_commands.Choice(name='Yellow', value=24)
    ])
    async def embed(self, interaction: discord.Interaction, title: str, description: str, color: discord.app_commands.Choice[int]):
        color_mapping = {
        'Aqua': (26, 188, 156),
        'Dark Aqua': (17, 128, 106),
        'Green': (87, 242, 135),
        'Dark Green': (31, 139, 76),
        'Blue': (52, 152, 219),
        'Dark Blue': (32, 102, 147),
        'Purple': (155, 89, 182),
        'Dark Purple': (113, 54, 138),
        'Luminous Vivid Pink': (233, 30, 99),
        'Dark Vivid Pink': (173, 20, 87),
        'Gold': (241, 196, 15),
        'Dark Gold': (194, 124, 14),
        'Orange': (230, 126, 34),
        'Dark Orange': (168, 67, 0),
        'Red': (237, 66, 69),
        'Dark Red': (153, 45, 34),
        'Grey': (149, 165, 166),
        'Dark Grey': (151, 156, 159),
        'Darker Grey': (127, 140, 141),
        'Light Grey': (188, 192, 192),
        'Navy': (52, 73, 94),
        'Dark Navy': (44, 62, 80),
        'Yellow': (255, 255, 0)
        }

        def rgb_to_discord_colour(rgb):
            return discord.Colour.from_rgb(*rgb)
        
        if color.name in color_mapping:
            embed_color = rgb_to_discord_colour(color_mapping[color.name])
        else:
            # Default color if the color name is not found
            embed_color = discord.Colour.blurple()

        try:
            embed = discord.Embed(
                color=embed_color,
                title=title,
                description=description)
            if interaction.user.id == config.OWNER_ID:
                # admin version does not show slash command used
                await interaction.response.send_message(content='Embed created, deleting in 5 seconds...', ephemeral=True, delete_after=5)
                await interaction.channel.send(embed=embed)
            else:
                await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content='Error occured.')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(embed(client))