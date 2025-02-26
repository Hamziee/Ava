import sqlite3

DB_PATH = "databases/locale.db"

def setup_database():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_locale (
                    user_id INTEGER PRIMARY KEY,
                    locale TEXT)''')
    conn.commit()
    conn.close()

def getLang(user_id: int) -> str:
    """Retrieve the preferred language of the user. Defaults to en_US."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT locale FROM user_locale WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "en_US"  # Default to English

def setLang(user_id: int, locale: str):
    """Set or update the preferred language for a user."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO user_locale (user_id, locale) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET locale = ?", 
              (user_id, locale, locale))
    conn.commit()
    conn.close()

# Ensure the database is set up when this module is imported
setup_database()
