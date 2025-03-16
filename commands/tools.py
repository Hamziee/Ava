import discord
from discord.ext import commands
from discord import app_commands
import config
from i18n import i18n

class toolsCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    
    tools = app_commands.Group(name="tools", description="Useful tools.")
    
    @tools.command(name="userinfo", description="See all public available user information.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def userinfo(self, interaction: discord.Interaction, member: discord.User):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('tools', user_locale)
       
        fetched_member = await self.client.fetch_user(member.id)
       
        embed = discord.Embed(
            color=discord.Colour.blurple()
        )
        general_info = f"{lang.userinfo_ID}: {member.id}\n"
        general_info += f"{lang.userinfo_username}: {member.name}\n"
        if member.bot == True:
            isBot = lang.userinfo_yes
        else:
            isBot = lang.userinfo_no
        general_info += f"{lang.userinfo_bot}: {isBot}\n"
        
        # Get highest resolution avatar (4096px)
        if member.avatar:
            if "?size=" in member.avatar.url:
                high_res_avatar = member.avatar.url.split("?size=")[0] + "?size=4096"
            else:
                high_res_avatar = member.avatar.url + "?size=4096"
            high_res_avatar = high_res_avatar.replace(".webp", ".png")
        else:
            high_res_avatar = member.default_avatar.url
        
        embed.set_thumbnail(url=high_res_avatar)
        
        # Get highest resolution banner (4096px) if it exists
        if fetched_member.banner:
            if "?size=" in fetched_member.banner.url:
                high_res_banner = fetched_member.banner.url.split("?size=")[0] + "?size=4096"
            else:
                high_res_banner = fetched_member.banner.url + "?size=4096"
            high_res_banner = high_res_banner.replace(".webp", ".png")
            
            embed.set_image(url=high_res_banner)
            ifBanner = f"[{lang.userinfo_banner_download}]({high_res_banner})\n"
        else:
            embed.set_image(url="https://example.com/default_banner.png")
            ifBanner = f"{lang.userinfo_no_banner}\n"
           
        embed.add_field(name=lang.userinfo_generalinfo, value=general_info, inline=False)
        embed.add_field(name=lang.userinfo_account_created, value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        try:
            joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
        except AttributeError:
            joined_at = lang.userinfo_notInAServer
        embed.add_field(name=lang.userinfo_joined_guild, value=joined_at, inline=True)
        embed.add_field(name=lang.userinfo_downloads, value=f"[{lang.userinfo_avatar_download}]({high_res_avatar})\n{ifBanner}", inline=False)
        embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.send_message(content="", embed=embed)

    @tools.command(name="serverinfo", description="See all public available server information.")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    async def serverinfo(self, interaction: discord.Interaction):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('tools', user_locale)
        
        guild = interaction.guild
        fetched_guild = await self.client.fetch_guild(guild.id, with_counts=True)
        guild_owner = await self.client.fetch_user(guild.owner_id)
        
        embed = discord.Embed(
            title=guild.name,
            description=guild.description if guild.description else lang.serverinfo_no_description,
            color=discord.Colour.blurple()
        )
        
        # Get highest resolution guild icon (4096px)
        if guild.icon:
            if "?size=" in guild.icon.url:
                high_res_icon = guild.icon.url.split("?size=")[0] + "?size=4096"
            else:
                high_res_icon = guild.icon.url + "?size=4096"
            high_res_icon = high_res_icon.replace(".webp", ".png")
            
            embed.set_thumbnail(url=high_res_icon)
            guild_icon_download = f"[{lang.serverinfo_icon_download}]({high_res_icon})\n"
        else:
            guild_icon_download = f"{lang.serverinfo_no_icon}\n"
        
        # Get highest resolution guild banner (4096px) if it exists
        if guild.banner:
            if "?size=" in guild.banner.url:
                high_res_banner = guild.banner.url.split("?size=")[0] + "?size=4096"
            else:
                high_res_banner = guild.banner.url + "?size=4096"
            high_res_banner = high_res_banner.replace(".webp", ".png")
            
            embed.set_image(url=high_res_banner)
            guild_banner_download = f"[{lang.serverinfo_banner_download}]({high_res_banner})\n"
        else:
            guild_banner_download = f"{lang.serverinfo_no_banner}\n"
        
        # General server information
        general_info = f"{lang.serverinfo_ID}: {guild.id}\n"
        general_info += f"{lang.serverinfo_owner}: {guild_owner.name} ({guild_owner.id})\n"
        general_info += f"{lang.serverinfo_created}: {guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        general_info += f"{lang.serverinfo_members}: {guild.member_count}\n"
        
        # Boost status
        boost_info = f"{lang.serverinfo_level}: {guild.premium_tier}\n"
        boost_info += f"{lang.serverinfo_boosts}: {guild.premium_subscription_count}\n"
        
        # Features list
        if guild.features:
            features_list = ", ".join([feature.replace("_", " ").title() for feature in guild.features])
        else:
            features_list = lang.serverinfo_no_features
            
        embed.add_field(name=lang.serverinfo_generalinfo, value=general_info, inline=False)
        embed.add_field(name=lang.serverinfo_boost, value=boost_info, inline=True)
        embed.add_field(name=lang.serverinfo_features, value=features_list, inline=True)
        embed.add_field(name=lang.serverinfo_downloads, value=f"{guild_icon_download}{guild_banner_download}", inline=False)
        
        # Add server splash image if it exists
        if guild.splash:
            if "?size=" in guild.splash.url:
                high_res_splash = guild.splash.url.split("?size=")[0] + "?size=4096"
            else:
                high_res_splash = guild.splash.url + "?size=4096"
            high_res_splash = high_res_splash.replace(".webp", ".png")
            
            embed.add_field(name=lang.serverinfo_splash, value=f"[{lang.serverinfo_splash_download}]({high_res_splash})", inline=True)
        
        # Add discovery splash if it exists
        if hasattr(guild, 'discovery_splash') and guild.discovery_splash:
            if "?size=" in guild.discovery_splash.url:
                high_res_discovery = guild.discovery_splash.url.split("?size=")[0] + "?size=4096"
            else:
                high_res_discovery = guild.discovery_splash.url + "?size=4096"
            high_res_discovery = high_res_discovery.replace(".webp", ".png")
            
            embed.add_field(name=lang.serverinfo_discovery, value=f"[{lang.serverinfo_discovery_download}]({high_res_discovery})", inline=True)
            
        embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.send_message(content="", embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(toolsCog(client))