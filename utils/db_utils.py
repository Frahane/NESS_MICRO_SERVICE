import sqlite3
import logging
from datetime import datetime

# Enable logging for database operations
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Establish a database connection.
    """
    try:
        conn = sqlite3.connect('users.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        return None

def add_user(telegram_id, username):
    """
    Add a new user to the database.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (telegram_id, username) VALUES (?, ?)', (telegram_id, username))
            conn.commit()
            logger.info(f"User added: {username} with ID: {telegram_id}")
        except sqlite3.Error as e:
            logger.error(f"Error adding user: {e}")
        finally:
            conn.close()

def log_fallback_usage(tx_hash, method):
    """
    Log when web scraping is used as a fallback.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO fallback_logs (tx_hash, method, timestamp)
                VALUES (?, ?, ?)
            ''', (tx_hash, method, datetime.now()))
            conn.commit()
            logger.info(f"Fallback method used: {method} for transaction {tx_hash}")
        except sqlite3.Error as e:
            logger.error(f"Error logging fallback usage: {e}")
        finally:
            conn.close()

def update_ness_balance(telegram_id, new_balance):
    """
    Update a user's NESS balance.
    """
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET ness_balance = ? WHERE telegram_id = ?', (new_balance, telegram_id))
            conn.commit()
            logger.info(f"Updated NESS balance for user ID: {telegram_id} to {new_balance}")
        except sqlite3.Error as e:
            logger.error(f"Error updating NESS balance: {e}")
        finally:
            conn.close()


# Initialize the database (create tables if they don't exist)
def initialize_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bot_subscriptions (
                    telegram_id INTEGER,
                    bot_name TEXT,
                    bot_username TEXT,
                    payment_address TEXT,
                    expires_at DATETIME,
                    PRIMARY KEY (telegram_id, bot_name)
                )
            ''')
            conn.commit()
            logger.info("Database initialized successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")
        finally:
            conn.close()
    else:
        logger.error("Failed to initialize database. No connection established.")

# Save bot subscription to the database
def save_bot_subscription(subscription):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO bot_subscriptions (telegram_id, bot_name, bot_username, payment_address, expires_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (subscription['telegram_id'], subscription['bot_name'], subscription['bot_username'], subscription['payment_address'], subscription['expires_at']))
            conn.commit()
            logger.info(f"Saved subscription for user ID: {subscription['telegram_id']} to bot: {subscription['bot_name']}.")
        except sqlite3.Error as e:
            logger.error(f"Error saving subscription: {e}")
        finally:
            conn.close()

# Get user bot subscription
def get_user_bot_subscription(telegram_id, bot_name):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM bot_subscriptions
                WHERE telegram_id = ? AND bot_name = ?
            ''', (telegram_id, bot_name))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"Error retrieving subscription: {e}")
            return None
        finally:
            conn.close()

# Remove bot subscription
def remove_bot_subscription(telegram_id, bot_name):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM bot_subscriptions
                WHERE telegram_id = ? AND bot_name = ?
            ''', (telegram_id, bot_name))
            conn.commit()
            logger.info(f"Removed subscription for user ID: {telegram_id} from bot: {bot_name}.")
        except sqlite3.Error as e:
            logger.error(f"Error removing subscription: {e}")
        finally:
            conn.close()