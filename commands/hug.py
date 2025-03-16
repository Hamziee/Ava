import discord
from discord.ext import commands
from discord import app_commands
import httpx
import config
from i18n import i18n

class hug(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="hug", description="Hug your friend/lover!")
    @app_commands.rename(member='person')
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def hug(self, interaction: discord.Interaction, member: discord.User):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('hug', user_locale)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.hamzie.site/v1/gifs/hug")
                response.raise_for_status()
                data = response.json()
                image_url = data["link"]
                
                desctxt = f"{interaction.user.mention} {lang.gives_hug} {member.mention} <:AVA_hug:1244799683042344970>"
                if member.id == interaction.user.id:
                    desctxt = f"{lang.hug_toself} <a:ava_CatCuddle:1244799986600902758>"
                elif member.id == config.BOT_ID:
                    desctxt = f"{lang.hug_toava} <a:AVA_hugg:1244799800378130472>"
                elif member.bot:
                    desctxt = f"{lang.hug_toabot} <a:AVA_cats_hug:1244799755960451159>"

                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    description=desctxt
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION} - {lang.by}: hamzie.site/api", icon_url=config.FOOTER_ICON)
                await interaction.response.send_message(embed=embed)

        except httpx.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')

async def setup(client:commands.Bot) -> None:
    await client.add_cog(hug(client))