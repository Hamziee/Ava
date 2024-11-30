import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import random
import asyncio
import config

class Games(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="trivia", description="Test your knowledge with a trivia question!")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def trivia(self, interaction: discord.Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://opentdb.com/api.php?amount=1&type=multiple") as response:
                    data = await response.json()
                    if data["response_code"] != 0:
                        await interaction.response.send_message(content="Failed to fetch trivia question. Please try again later.")
                        return

                    question_data = data["results"][0]
                    question = question_data["question"]
                    correct_answer = question_data["correct_answer"]
                    incorrect_answers = question_data["incorrect_answers"]
                    options = incorrect_answers + [correct_answer]
                    random.shuffle(options)

                    embed = discord.Embed(
                        color=discord.Colour.blurple(),
                        title="🧠 Trivia Time!",
                        description=f"{question}\n\nSelect the correct option by typing the number (1-{len(options)}):"
                    )
                    for i, option in enumerate(options, 1):
                        embed.add_field(name=f"Option {i}", value=option, inline=False)
                    embed.set_footer(
                        text=config.FOOTER_TXT + " - You have 30 seconds to respond!",
                        icon_url=config.FOOTER_ICON
                    )
                    await interaction.response.send_message(embed=embed)

                    def check(message: discord.Message):
                        return (
                            message.author == interaction.user
                            and message.content.isdigit()
                            and 1 <= int(message.content) <= len(options)
                        )

                    try:
                        user_response = await self.client.wait_for("message", check=check, timeout=30.0)
                        user_choice = int(user_response.content) - 1
                        if options[user_choice] == correct_answer:
                            await interaction.followup.send(content=f"🎉 Correct! The answer was **{correct_answer}**.")
                        else:
                            await interaction.followup.send(content=f"❌ Wrong! The correct answer was **{correct_answer}**.")
                    except asyncio.TimeoutError:
                        await interaction.followup.send(content=f"⏰ Time's up! The correct answer was **{correct_answer}**.")

        except Exception as e:
            print(e)
            await interaction.response.send_message(content="An error occurred while running the trivia game.")

    @app_commands.command(name="typerace", description="Test your typing skills in a type race!")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def typerace(self, interaction: discord.Interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://fakerapi.it/api/v1/texts?_quantity=1&_characters=150") as response:
                    if response.status != 200:
                        await interaction.response.send_message(content="Failed to fetch a typing challenge. Try again later!")
                        return

                    data = await response.json()
                    sentence = data["data"][0]["content"]
                    sentence = sentence.replace("'", "").strip()

            embed = discord.Embed(
                color=discord.Colour.blurple(),
                title="⌨️ Type Race",
                description=f"Type the following sentence as fast as you can:\n\n**{sentence}**"
            )
            embed.set_footer(text=config.FOOTER_TXT + " - Start typing now!")
            await interaction.response.send_message(embed=embed)

            def check(message: discord.Message):
                return message.author == interaction.user

            try:
                start_time = asyncio.get_event_loop().time()
                user_response = await self.client.wait_for("message", check=check, timeout=60.0)
                end_time = asyncio.get_event_loop().time()

                if user_response.content == sentence:
                    time_taken = end_time - start_time
                    await interaction.followup.send(content=f"🎉 Well done! You typed the sentence in **{time_taken:.2f} seconds**.")
                else:
                    await interaction.followup.send(content="❌ Incorrect! Try again next time.")
            except asyncio.TimeoutError:
                await interaction.followup.send(content="⏰ Time's up! Better luck next time.")

        except Exception as e:
            print(e)
            await interaction.response.send_message(content="An error occurred while running the type race.")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Games(client))