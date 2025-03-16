import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from datetime import datetime, timedelta
import config
from i18n import i18n
from databases.database import (
    get_balance, 
    update_balance, 
    log_transaction, 
    can_work, 
    update_work_status,
    get_all_balances
)

class BlackjackView(discord.ui.View):
    def __init__(self, timeout=30):
        super().__init__(timeout=timeout)
        self.value = None

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "hit"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "stand"
        self.stop()
        await interaction.response.defer()

class Economy(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="balance", description="Check your or someone else's balance")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('economy', user_locale)

        target_user = member or interaction.user
        balance = get_balance(target_user.id)
        embed = discord.Embed(
            color=discord.Colour.green(),
            title=lang.balance_title.format(username=target_user.name),
            description=f"{lang.balance_text}: **{balance:.2f}** {lang.currency}"
        )
        embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="work", description="Work to earn money")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def work(self, interaction: discord.Interaction):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('economy', user_locale)

        if not can_work(interaction.user.id):
            await interaction.response.send_message(content=lang.work_cooldown)
            return

        earnings = round(random.uniform(50, 200), 2)
        update_work_status(interaction.user.id, earnings)

        embed = discord.Embed(
            color=discord.Colour.green(),
            title=lang.work_title,
            description=f"{lang.work_success.format(earnings=earnings, currency=lang.currency)}"
        )
        embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pay", description="Send money to another user")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def pay(self, interaction: discord.Interaction, user: discord.User, amount: float):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('economy', user_locale)

        if user.id == interaction.user.id:
            await interaction.response.send_message(content=lang.pay_self_error)
            return

        sender_balance = get_balance(interaction.user.id)
        if sender_balance < amount or amount <= 0:
            await interaction.response.send_message(content=lang.insufficient_balance)
            return

        update_balance(interaction.user.id, -amount)
        update_balance(user.id, amount)
        log_transaction(interaction.user.id, user.id, amount)

        embed = discord.Embed(
            color=discord.Colour.green(),
            title=lang.pay_title,
            description=f"{lang.pay_success.format(sender=interaction.user.name, recipient=user.name, amount=amount, currency=lang.currency)}"
        )
        embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="coinflip", description="Bet on heads or tails")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.choices(choice=[
        app_commands.Choice(name="Heads", value="heads"),
        app_commands.Choice(name="Tails", value="tails")
    ])
    async def coinflip(self, interaction: discord.Interaction, choice: app_commands.Choice[str], amount: float):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('economy', user_locale)

        user_balance = get_balance(interaction.user.id)
        if user_balance < amount or amount <= 0:
            await interaction.response.send_message(content=lang.insufficient_balance)
            return

        if random.randint(1, 1000) == 1:
            winnings = amount * 100
            update_balance(interaction.user.id, winnings - amount)
            result_message = lang.coinflip_side.format(winnings=winnings, currency=lang.currency)
            color = discord.Colour.gold()
        else:
            result = random.choice(['heads', 'tails'])
            
            if choice.value == result:
                winnings = amount * 2
                update_balance(interaction.user.id, winnings - amount)
                result_message = lang.coinflip_win.format(result=result, winnings=winnings, currency=lang.currency)
                color = discord.Colour.green()
            else:
                update_balance(interaction.user.id, -amount)
                result_message = lang.coinflip_lose.format(result=result, amount=amount, currency=lang.currency)
                color = discord.Colour.red()

        embed = discord.Embed(
            color=color,
            title=lang.coinflip_title,
            description=result_message
        )
        embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="blackjack", description="Play a game of Blackjack")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def blackjack(self, interaction: discord.Interaction, bet: float):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('economy', user_locale)

        user_balance = get_balance(interaction.user.id)
        if user_balance < bet or bet <= 0:
            await interaction.response.send_message(content=lang.insufficient_balance)
            return

        def create_deck():
            suits = ['♠️', '♥️', '♦️', '♣️']
            ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            return [f"{rank}{suit}" for suit in suits for rank in ranks] * 4

        def card_value(card):
            rank = ''.join(char for char in card if char.isalnum())
            
            if rank in ['J', 'Q', 'K']:
                return 10
            elif rank == 'A':
                return 11
            else:
                return int(rank)

        def calculate_hand(hand):
            value = sum(card_value(card) for card in hand)
            aces = sum(1 for card in hand if 'A' in card)
            
            while value > 21 and aces:
                value -= 10
                aces -= 1
            
            return value

        deck = create_deck()
        random.shuffle(deck)
        
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        embed = discord.Embed(
            color=discord.Colour.blurple(),
            title=lang.blackjack_title
        )
        embed.add_field(name=lang.blackjack_your_hand, value=f"{' '.join(player_hand)} ({lang.blackjack_total}: {calculate_hand(player_hand)})", inline=False)
        embed.add_field(name=lang.blackjack_dealer_hand, value=f"{dealer_hand[0]} 🂠", inline=False)
        embed.add_field(name=lang.blackjack_bet, value=f"{bet} {lang.currency}", inline=False)
        embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
        
        view = BlackjackView()
        await interaction.response.send_message(embed=embed, view=view)
        message = await interaction.original_response()

        try:
            while calculate_hand(player_hand) < 21:
                view = BlackjackView()
                await message.edit(embed=embed, view=view)
                
                await view.wait()
                if view.value is None:
                    await interaction.followup.send(content=lang.blackjack_timeout)
                    return
                
                if view.value == "hit":
                    player_hand.append(deck.pop())
                    player_total = calculate_hand(player_hand)
                    
                    embed = discord.Embed(
                        color=discord.Colour.blurple(),
                        title=lang.blackjack_title
                    )
                    embed.add_field(name=lang.blackjack_your_hand, value=f"{' '.join(player_hand)} ({lang.blackjack_total}: {player_total})", inline=False)
                    embed.add_field(name=lang.blackjack_dealer_hand, value=f"{dealer_hand[0]} 🂠", inline=False)
                    embed.add_field(name=lang.blackjack_bet, value=f"{bet} {lang.currency}", inline=False)
                    embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
                    
                    if player_total > 21:
                        break
                else:
                    break

            # Remove buttons from the final message
            player_total = calculate_hand(player_hand)
            if player_total <= 21:
                while calculate_hand(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())

            dealer_total = calculate_hand(dealer_hand)

            if player_total > 21:
                result = lang.blackjack_bust
                update_balance(interaction.user.id, -bet)
                color = discord.Colour.red()
            elif dealer_total > 21:
                result = lang.blackjack_dealer_bust
                update_balance(interaction.user.id, bet)
                color = discord.Colour.green()
            elif player_total > dealer_total:
                result = lang.blackjack_win_higher.format(player_total=player_total, dealer_total=dealer_total)
                update_balance(interaction.user.id, bet)
                color = discord.Colour.green()
            elif player_total < dealer_total:
                result = lang.blackjack_lose_lower.format(player_total=player_total, dealer_total=dealer_total)
                update_balance(interaction.user.id, -bet)
                color = discord.Colour.red()
            else:
                result = lang.blackjack_push.format(total=player_total)
                color = discord.Colour.blue()

            embed = discord.Embed(
                color=color,
                title=lang.blackjack_result_title
            )
            embed.add_field(name=lang.blackjack_your_hand, value=f"{' '.join(player_hand)} ({lang.blackjack_total}: {player_total})", inline=False)
            embed.add_field(name=lang.blackjack_dealer_hand, value=f"{' '.join(dealer_hand)} ({lang.blackjack_total}: {dealer_total})", inline=False)
            embed.add_field(name=lang.blackjack_result, value=result, inline=False)
            embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await message.edit(embed=embed, view=None)

        except Exception as e:
            print(f"Error in blackjack command: {e}")
            await interaction.followup.send(content=lang.blackjack_error)

    @app_commands.command(name="leaderboard", description="View the economy leaderboard")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.choices(scope=[
        app_commands.Choice(name="Global", value="global"),
        app_commands.Choice(name="Server", value="server")
    ])
    async def leaderboard(self, interaction: discord.Interaction, scope: app_commands.Choice[str]):
        user_locale = i18n.get_locale(interaction.user.id)
        lang = i18n.get_module('economy', user_locale)

        if scope.value == "server" and not interaction.guild:
            await interaction.response.send_message(content=lang.server_leaderboard_error)
            return

        await interaction.response.defer()

        try:
            if scope.value == "server":
                member_ids = [member.id for member in interaction.guild.members]
                title = lang.server_leaderboard_title.format(server=interaction.guild.name)
                balances = [(user_id, get_balance(user_id)) for user_id in member_ids]
            else:
                balances = get_all_balances()
                title = lang.global_leaderboard_title

            top_balances = sorted(balances, key=lambda x: x[1], reverse=True)[:10]

            if not top_balances:
                await interaction.followup.send(content=lang.leaderboard_empty)
                return

            embed = discord.Embed(
                color=discord.Colour.blue(),
                title=title,
                description=lang.leaderboard_description
            )

            for i, (user_id, balance) in enumerate(top_balances, 1):
                try:
                    user = await self.client.fetch_user(user_id)
                    name = user.name
                except discord.NotFound:
                    name = lang.unknown_user
                
                medal = ""
                if i == 1:
                    medal = "🥇 "
                elif i == 2:
                    medal = "🥈 "
                elif i == 3:
                    medal = "🥉 "
                
                embed.add_field(
                    name=f"{medal}#{i} {name}",
                    value=f"{balance:.2f} {lang.currency}",
                    inline=False
                )

            embed.set_footer(text=f"Ava | {lang.version}: {config.AVA_VERSION}", icon_url=config.FOOTER_ICON)
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"Error in leaderboard command: {e}")
            await interaction.followup.send(content=lang.leaderboard_error)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Economy(client))