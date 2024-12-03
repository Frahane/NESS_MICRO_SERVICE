import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    DB_PATH = 'users.db'
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'
    WEBAPP_URL = os.getenv('WEBAPP_URL') 