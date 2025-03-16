import mysql.connector
from datetime import datetime, timedelta
import config

def get_locale_connection():
    """Get connection to locale database"""
    return mysql.connector.connect(**config.LOCALE_DB)

def get_economy_connection():
    """Get connection to economy database"""
    return mysql.connector.connect(**config.ECONOMY_DB)

def get_economylog_connection():
    """Get connection to economy log database"""
    return mysql.connector.connect(**config.ECONOMYLOG_DB)

def setup_database():
    """Initialize the databases and create tables if they don't exist."""
    # Locale database setup
    conn = get_locale_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_locale (
                    user_id BIGINT PRIMARY KEY,
                    locale VARCHAR(10) NOT NULL)''')
    conn.commit()
    conn.close()

    # Economy database setup
    conn = get_economy_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_economy (
                    user_id BIGINT PRIMARY KEY,
                    balance DECIMAL(10,2) DEFAULT 0,
                    last_work TIMESTAMP NULL,
                    work_streak INT DEFAULT 0)''')
    conn.commit()
    conn.close()

    # Economy log database setup
    conn = get_economylog_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    sender_id BIGINT NOT NULL,
                    recipient_id BIGINT NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Locale functions
def get_lang(user_id: int) -> str:
    """Retrieve the preferred language of the user. Defaults to en_US."""
    conn = get_locale_connection()
    c = conn.cursor()
    c.execute("SELECT locale FROM user_locale WHERE user_id = %s", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "en_US"  # Default to English

def set_lang(user_id: int, locale: str):
    """Set or update the preferred language for a user."""
    conn = get_locale_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO user_locale (user_id, locale) 
                 VALUES (%s, %s) 
                 ON DUPLICATE KEY UPDATE locale = %s""", 
              (user_id, locale, locale))
    conn.commit()
    conn.close()

# Economy functions
def get_balance(user_id: int) -> float:
    """Retrieve the user's current balance."""
    conn = get_economy_connection()
    c = conn.cursor()
    c.execute("SELECT balance FROM user_economy WHERE user_id = %s", (user_id,))
    result = c.fetchone()
    conn.close()
    return float(result[0]) if result else 0.0

def update_balance(user_id: int, amount: float):
    """Update user's balance. Can be positive (add) or negative (subtract)."""
    conn = get_economy_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO user_economy (user_id, balance) 
                 VALUES (%s, %s) 
                 ON DUPLICATE KEY UPDATE balance = balance + %s""",
              (user_id, amount, amount))
    conn.commit()
    conn.close()

def log_transaction(sender_id: int, recipient_id: int, amount: float):
    """Log a transaction between users."""
    conn = get_economylog_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO transactions (sender_id, recipient_id, amount) 
                 VALUES (%s, %s, %s)""",
              (sender_id, recipient_id, amount))
    conn.commit()
    conn.close()

def can_work(user_id: int) -> bool:
    """Check if user can work (10-minute cooldown)."""
    conn = get_economy_connection()
    c = conn.cursor()
    c.execute("SELECT last_work, work_streak FROM user_economy WHERE user_id = %s", (user_id,))
    result = c.fetchone()
    conn.close()
    
    if not result:
        return True
    
    last_work, work_streak = result
    if not last_work:
        return True
    
    return datetime.now() - last_work >= timedelta(minutes=10)

def update_work_status(user_id: int, earnings: float):
    """Update work status after successful work."""
    conn = get_economy_connection()
    c = conn.cursor()
    now = datetime.now()
    c.execute("""INSERT INTO user_economy (user_id, balance, last_work, work_streak) 
                 VALUES (%s, %s, %s, 1)
                 ON DUPLICATE KEY UPDATE 
                    balance = balance + %s,
                    last_work = %s,
                    work_streak = work_streak + 1""",
              (user_id, earnings, now, earnings, now))
    conn.commit()
    conn.close()

def get_all_balances() -> list:
    """Get all user balances from the database."""
    conn = get_economy_connection()
    c = conn.cursor()
    c.execute("""SELECT user_id, balance 
                 FROM user_economy 
                 WHERE balance > 0 
                 ORDER BY balance DESC""")
    results = c.fetchall()
    conn.close()
    return results

# Initialize the databases when this module is imported
setup_database() 