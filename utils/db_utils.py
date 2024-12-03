import sqlite3
import logging

# Enable logging for database operations
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# Connect to the database
def get_db_connection():
    try:
        conn = sqlite3.connect('users.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row  # This allows for dictionary-like row access
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        return None

# Initialize the database (create tables if they don't exist)
def initialize_db():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY,
                    username TEXT,
                    ness_balance REAL DEFAULT 0,
                    locked_ness REAL DEFAULT 0,
                    coin_hour_balance REAL DEFAULT 0
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

# Add or update user in the database
def add_user(telegram_id, username):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (telegram_id, username)
                VALUES (?, ?)
            ''', (telegram_id, username))
            conn.commit()
            logger.info(f"User {username} (ID: {telegram_id}) added or updated.")
        except sqlite3.Error as e:
            logger.error(f"Error adding/updating user: {e}")
        finally:
            conn.close()

# Update NESS balance for a user
def update_ness_balance(telegram_id, amount):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users
                SET ness_balance = ness_balance + ?
                WHERE telegram_id = ?
            ''', (amount, telegram_id))
            conn.commit()
            logger.info(f"Updated NESS balance for user ID: {telegram_id}. Amount: {amount}.")
        except sqlite3.Error as e:
            logger.error(f"Error updating NESS balance: {e}")
        finally:
            conn.close()

# Lock a certain amount of NESS for a user
def lock_ness(telegram_id, amount):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users
                SET locked_ness = locked_ness + ?
                WHERE telegram_id = ?
            ''', (amount, telegram_id))
            conn.commit()
            logger.info(f"Locked {amount} NESS for user ID: {telegram_id}.")
        except sqlite3.Error as e:
            logger.error(f"Error locking NESS: {e}")
        finally:
            conn.close()

# Unlock a certain amount of NESS for a user
def unlock_ness(telegram_id, amount):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users
                SET locked_ness = locked_ness - ?
                WHERE telegram_id = ?
            ''', (amount, telegram_id))
            conn.commit()
            logger.info(f"Unlocked {amount} NESS for user ID: {telegram_id}.")
        except sqlite3.Error as e:
            logger.error(f"Error unlocking NESS: {e}")
        finally:
            conn.close()

# Update the Coin Hour balance for a user
def update_coin_hour_balance(telegram_id, amount):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users
                SET coin_hour_balance = coin_hour_balance + ?
                WHERE telegram_id = ?
            ''', (amount, telegram_id))
            conn.commit()
            logger.info(f"Updated Coin Hour balance for user ID: {telegram_id}. Amount: {amount}.")
        except sqlite3.Error as e:
            logger.error(f"Error updating Coin Hour balance: {e}")
        finally:
            conn.close()