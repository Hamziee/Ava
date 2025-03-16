AVA_VERSION = 'v1.0.0-stable' # Do not change this, it will help with troubleshooting later
CONFIG_VERSION = 5 # Do not change this, it will help with troubleshooting later

# Required Bot Configuration
# Configuring this to your bot's settings is crucial for the bot to function properly.

PREFIX = '$' # deprecated, only used for admin commands.
OWNER_ID = 496673945211240462 # used for admin commands and ChatAI recognition
PERMISSION_DENIED = 'You do not have permission to run this command.' # copied from my old bot, unused for now
STATUS = AVA_VERSION # Want a custom status? Replace it with: STATUS = 'your status here'
FOOTER_TXT = "Ava" # This will be displayed in the footer of every embed
FOOTER_ICON = 'https://cdn.discordapp.com/avatars/1209925239652356147/38e76bc9070eb00f2493b6edeab22b33.webp' # Put your bot's avatar URL here or an image of your choice
BOT_ID = 1209925239652356147 # Put your bot's ID here
TOKEN = 'Put your Discord bot token here.'
COMMANDS_DIRECTORY = 'commands'

# Database Configuration (If every DB is on the same server, you can use these variables. If not, you can use the HOST & PORT variables in each DB.)
DB_HOST = 'hamzie.site'
DB_PORT = 3306

# Locale Database
LOCALE_DB = {
    'host': DB_HOST,
    'port': DB_PORT,
    'database': 'database',
    'user': 'user',
    'password': 'password'
}

# Economy Database
ECONOMY_DB = {
    'host': DB_HOST,
    'port': DB_PORT,
    'database': 'database',
    'user': 'user',
    'password': 'password'
}

# Economy Log Database
ECONOMYLOG_DB = {
    'host': DB_HOST,
    'port': DB_PORT,
    'database': 'database',
    'user': 'user',
    'password': 'password'
}

# Optional Bot Configuration
# Configuring this to your bot's settings is optional, but it can enhance the bot's functionality. Make sure to disable commands that require these settings if you don't configure them.

THECATAPI_KEY = 'your thecatapi key here' # Get your own free key at https://thecatapi.com/