import discord
from discord.ext import commands
from discord import app_commands
import random
import config

class Fun(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="ball", description="Get the truth of your question.")
    async def ball(self, interaction: discord.Interaction, question: str):
        try:
            responses = [
                "Yes, definitely!",
                "No, absolutely not.",
                "Ask again later.",
                "It is certain.",
                "I wouldn't count on it.",
                "Most likely.",
                "Outlook not so good.",
                "Better not tell you now.",
                "Yes!",
                "My sources say no."
            ]
            answer = random.choice(responses)
            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title=f"🎱 Question: {question}",
                description=f"**Answer:** {answer}"
            )
            embed.set_footer(text=f"Ava | version: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send(content='An error occurred.')

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Fun(client))
