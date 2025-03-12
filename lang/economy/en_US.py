# Source file for strings.
# File version: v2.0
# - x.0 → Increment x by 1 if new string(s) are added or removed.
# - 0.x → Increment x by 1 if existing string(s) are changed or removed.
# A language needs translation if the language version doesn't match this version. This file (en_US.py) is always the source file for any translation.
# Please make sure to check the bot's functionality after changing these strings.
# If you have any suggestions or improvements, please open a pull request!
# Thank you!

currency = "dollars"
version = "version"

# Balance command
balance_text = "Current balance"
balance_title = "💰 {username}'s Balance"

# Leaderboard command
global_leaderboard_title = "🌍 Global Economy Leaderboard"
server_leaderboard_title = "📊 {server} Economy Leaderboard"
server_leaderboard_error = "Server leaderboard can only be viewed in a server!"
leaderboard_empty = "No users found in the leaderboard yet!"
leaderboard_error = "An error occurred while fetching the leaderboard. Please try again later."
leaderboard_description = "Top 10 Richest Users"
unknown_user = "Unknown User"

# Work command
work_title = "💼 Work"
work_cooldown = "You can only work once every hour!"
work_success = "You worked hard and earned {earnings} {currency}!"

# Pay command
pay_title = "💸 Transaction"
pay_self_error = "You can't pay yourself!"
insufficient_balance = "Insufficient balance!"
pay_success = "{sender} paid {recipient} {amount} {currency}"

# Coinflip translations
coinflip_title = "🪙 Coinflip"
coinflip_invalid_choice = "Please choose either 'heads' or 'tails'!"
coinflip_win = "🎉 You won! It was {result}. You earned {winnings} {currency}!"
coinflip_lose = "😢 It was {result}. You lost {amount} {currency}."
coinflip_side = "🎊 INCREDIBLE! The coin landed on its side! You've won {winnings} {currency}! (1 in 1000 chance)"

# Blackjack translations
blackjack_title = "🃏 Blackjack"
blackjack_result_title = "🃏 Blackjack Result"
blackjack_your_hand = "Your Hand"
blackjack_your_total = "Your Total"
blackjack_dealer_hand = "Dealer's Hand"
blackjack_bet = "Bet"
blackjack_decision = "Type 'hit' to draw another card or 'stand' to keep your current hand."
blackjack_bust = "🃏 Bust! You went over 21."
blackjack_win = "🎉 You win! Dealer busted or your hand is higher."
blackjack_lose = "😢 Dealer wins. Your hand is lower."
blackjack_push = "📊 Push! It's a tie."
blackjack_timeout = "⏰ Game timed out. No action taken."