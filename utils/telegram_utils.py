import requests
from utils.config import Config
import logging
import json

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.token = Config.BOT_TOKEN
        self.chat_id = Config.CHAT_ID
        self.base_url = f'https://api.telegram.org/bot{self.token}'

    def send_message(self, chat_id, message, reply_markup=None):
        try:
            url = f'{self.base_url}/sendMessage'
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            if reply_markup:
                payload['reply_markup'] = json.dumps(reply_markup)
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return None

    def get_updates(self, offset=0):
        try:
            url = f'{self.base_url}/getUpdates'
            params = {
                'offset': offset,
                'timeout': 30,
                'allowed_updates': ['message', 'callback_query']
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get updates: {e}")
            return None

    def set_menu_button(self):
        try:
            url = f'{self.base_url}/setChatMenuButton'
            payload = { 
                'menu_button': {
                    'type': 'web_app',
                    'text': 'Trading',
                    'web_app': {'url': Config.WEBAPP_URL}
                }
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            # Add detailed logging
            logger.info(f"Set menu button response: {response.json()}")
            
            if response.status_code == 200:
                logger.info("Menu button set successfully")
            else:
                logger.error(f"Failed to set menu button. Status code: {response.status_code}")
                
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error setting menu button: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error setting menu button: {e}")
            return None

    def create_webapp_keyboard(self):
        return {
            'inline_keyboard': [[{
                'text': '🚀 Open Trading Dashboard',
                'web_app': {'url': Config.WEBAPP_URL}
            }]]
        }