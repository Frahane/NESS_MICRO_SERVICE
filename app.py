from flask import Flask, render_template, request, jsonify
from utils.config import Config
from utils.db_utils import add_user, update_ness_balance, initialize_db
from utils.telegram_utils import TelegramBot
import threading
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask app initialization
app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
bot = TelegramBot()

# Set up the menu button immediately after bot initialization
try:
    logger.info("Setting up Telegram menu button...")
    bot.set_menu_button()
    logger.info("Menu button setup completed")
except Exception as e:
    logger.error(f"Failed to set up menu button: {e}")

def process_update(update):
    """Process incoming updates from Telegram"""
    try:
        if 'message' not in update:
            return

        message = update['message']
        chat_id = message['chat']['id']
        user_id = message['from']['id']
        username = message['from'].get('username', '')
        text = message.get('text', '')

        if text == '/start':
            add_user(user_id, username)
            welcome_message = (
                "?? Welcome to PrivateNess Network Trading Automation!\n\n"
                "Click the button below to access your trading dashboard:"
            )
            keyboard = bot.create_webapp_keyboard()
            bot.send_message(chat_id, welcome_message, keyboard)
        elif text == '/help':
            help_message = (
                "?? Available Commands:\n"
                "/start - Open trading dashboard\n"
                "/balance - Check your NESS and NCH balance\n"
                "/help - Show this help message"
            )
            bot.send_message(chat_id, help_message)
        elif text == '/balance':
            balance_message = "Balance feature coming soon!"
            bot.send_message(chat_id, balance_message)

    except Exception as e:
        logger.error(f"Error processing update: {e}")

def poll_updates():
    """Continuous polling for updates"""
    offset = 0
    while True:
        try:
            updates = bot.get_updates(offset)
            if updates and updates.get('ok') and updates.get('result'):
                for update in updates['result']:
                    process_update(update)
                    offset = update['update_id'] + 1
            time.sleep(1)
        except Exception as e:
            logger.error(f"Error in polling loop: {e}")
            time.sleep(5)  # Wait before retrying

def setup():
    initialize_db()
    # Start polling thread
    polling_thread = threading.Thread(target=poll_updates)
    polling_thread.daemon = True
    polling_thread.start()
    
    # Try setting up menu button again in case it failed initially
    try:
        bot.set_menu_button()
    except Exception as e:
        logger.error(f"Failed to set up menu button in setup: {e}")

@app.route('/')
def home():
    try:
        return render_template('get_started.html')
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        return render_template('error.html', error=500), 500

@app.route('/telegram')
def telegram_web_app():
    try:
        return render_template('get_started.html')  # This is accessible by Telegram
    except Exception as e:
        logger.error(f"Error rendering telegram web app: {e}")
        return render_template('error.html', error=500), 500

@app.route('/telegram/services')  # Route for Telegram to access services
def telegram_services():
    try:
        return render_template('service.html')  # This is accessible by Telegram
    except Exception as e:
        logger.error(f"Error rendering service page: {e}")
        return render_template('error.html', error=500), 500

@app.route('/services')  # Regular route for web users
def services():
    try:
        return render_template('service.html')  # This is accessible by regular users
    except Exception as e:
        logger.error(f"Error rendering service page: {e}")
        return render_template('error.html', error=500), 500

@app.route('/about')  # Regular route for web users
def about():
    try:
        return render_template('about.html')  # This is accessible by regular users
    except Exception as e:
        logger.error(f"Error rendering about page: {e}")
        return render_template('error.html', error=500), 500

@app.route('/telegram/about')  # Route for Telegram to access services
def telegram_about():
    try:
        return render_template('about.html')  # This is accessible by Telegram
    except Exception as e:
        logger.error(f"Error rendering about page: {e}")
        return render_template('error.html', error=500), 500

@app.route('/contact')  # Regular route for web users
def contact():
    try:
        return render_template('contact.html')  # This is accessible by regular users
    except Exception as e:
        logger.error(f"Error rendering contact page: {e}")
        return render_template('error.html', error=500), 500

@app.route('/telegram/contact')  # Route for Telegram to access services
def telegram_contact():
    try:
        return render_template('contact.html')  # This is accessible by Telegram
    except Exception as e:
        logger.error(f"Error rendering contact page: {e}")
        return render_template('error.html', error=500), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=404), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error=500), 500

@app.route('/health')
def health_check():
    try:
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    try:
        # Run setup before starting the app
        setup()
        # Try setting menu button one more time before running the app
        bot.set_menu_button()
        app.run(debug=False, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.critical(f"Failed to start application: {e}")