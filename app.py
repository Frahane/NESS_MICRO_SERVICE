from flask import Flask, render_template, request, jsonify
from utils.config import Config
from utils.db_utils import add_user, update_ness_balance, initialize_db
from utils.telegram_utils import TelegramBot
from utils.payment_utils import BotAccessManager
import threading
import time
import logging

# Setup logging as early as possible
Config.setup_logging()

# Create logger for the application
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
    logger.info("Initializing PrivateNess Network Application")
    return app

# Flask app initialization
app = create_app()
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

bot_access_manager = BotAccessManager()

'''@app.route('/check_bot_access', methods=['POST'])
def check_bot_access():
    data = request.json
    telegram_id = data.get('telegram_id')
    bot_name = data.get('bot_name')

    # Check ongoing bot access
    access_result = bot_access_manager.check_ongoing_bot_access(
        telegram_id, 
        bot_name
    )
    
    logger.info(f"Access check result for {telegram_id} on {bot_name}: {access_result}")
    return jsonify(access_result)'''

@app.route('/telegram/check_bot_access', methods=['POST'])  # Telegram route
def check_bot_access():
    data = request.json
    telegram_id = data.get('telegram_id')
    bot_name = data.get('bot_name')

    # Check ongoing bot access
    access_result = bot_access_manager.check_ongoing_bot_access(telegram_id, bot_name)
    
    logger.info(f"Access check result for {telegram_id} on {bot_name}: {access_result}")
    return jsonify(access_result)


'''@app.route('/verify_bot_payment', methods=['POST'])
def verify_bot_payment():
    data = request.json
    telegram_id = data.get('telegram_id')
    bot_name = data.get('bot_name')
    tx_hash = data.get('tx_hash')

    # Verify bot access with transaction
    verification_result = bot_access_manager.verify_bot_access(
        telegram_id, 
        bot_name, 
        tx_hash
    )
    
    return jsonify(verification_result)'''

@app.route('/telegram/verify_bot_payment', methods=['POST'])  # Telegram route
def verify_bot_payment():
    data = request.json
    telegram_id = data.get('telegram_id')
    bot_name = data.get('bot_name')
    tx_hash = data.get('tx_hash')

    # Verify bot access with transaction
    verification_result = bot_access_manager.verify_bot_access(telegram_id, bot_name, tx_hash)
    
    return jsonify(verification_result)

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
        logger.info("Starting application on http://127.0.0.1:5000")
        initialize_db()  # Ensure the database is initialized
        app.run(
            host='0.0.0.0',  # Listen on all available interfaces
            port=5000,
            debug=False  # Ensure this is False in production
        )
    except Exception as e:
        logger.critical(f"Failed to start application: {e}", exc_info=True)
        logger.info(f"Checking bot access for user ID: {telegram_id}, bot name: {bot_name}")