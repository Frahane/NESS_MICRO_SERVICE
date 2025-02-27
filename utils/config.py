import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Centralized Configuration Management for PrivateNess Network
    """
    
    # Telegram Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    CHAT_ID = os.getenv('CHAT_ID')
    DB_PATH = os.getenv('DB_PATH', 'users.db')
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'
    WEBAPP_URL = os.getenv('WEBAPP_URL')

    # Blockchain Configuration
    PAYMENT_ADDRESS_DOGE_SPOT_BINANCE = os.getenv('PAYMENT_ADDRESS_DOGE_SPOT_BINANCE')
    PAYMENT_ADDRESS_DOGE_SPOT_KUCOIN = os.getenv('PAYMENT_ADDRESS_DOGE_SPOT_KUCOIN')
    PAYMENT_ADDRESS_DOGE_SPOT_OKX = os.getenv('PAYMENT_ADDRESS_DOGE_SPOT_OKX')
    PAYMENT_ADDRESS_XRP_SPOT_BINANCE = os.getenv('PAYMENT_ADDRESS_XRP_SPOT_BINANCE')
    PAYMENT_ADDRESS_DOGE_PERPETUAL_BINANCE = os.getenv('PAYMENT_ADDRESS_DOGE_PERPETUAL_BINANCE')
    PAYMENT_ADDRESS_DOGE_PERPETUAL_KUCOIN = os.getenv('PAYMENT_ADDRESS_DOGE_PERPETUAL_KUCOIN')
    PAYMENT_ADDRESS_DOGE_PERPETUAL_OKX = os.getenv('PAYMENT_ADDRESS_DOGE_PERPETUAL_OKX')
    PAYMENT_ADDRESS_XRP_PERPETUAL_BINANCE = os.getenv('PAYMENT_ADDRESS_XRP_PERPETUAL_BINANCE')
    # URLs Configuration
    RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:6660")
    EXPLORER_URL = os.getenv("EXPLORER_URL", "https://ness-explorer.magnetosphere.net")
    # Degging
    print(f"[DEBUG] Loaded EXPLORER_URL: {EXPLORER_URL}")

    # Payment and Subscription Configuration
    SUBSCRIPTION_DURATION_DAYS = 30
    REQUIRED_NCH = int(os.getenv('REQUIRED_NCH', 300000))
    MINIMUM_NESS = int(os.getenv('MINIMUM_NESS', 4000))


    # Comprehensive Bot Payment Configurations
    BOT_PAYMENT_CONFIGS: Dict[str, Dict[str, Any]] = {
        # Spot Trading Bots
        'Doge_Spot_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS_DOGE_SPOT_BINANCE,
            'bot_username': 'Stoneyard_Doge_Bot',
            'exchange': 'Binance',
            'trading_type': 'Spot'
        },
        'Doge_Spot_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS_DOGE_SPOT_KUCOIN,
            'bot_username': 'Stoneyard_Doge_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Spot'
        },
        'Doge_Spot_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS_DOGE_SPOT_OKX,
            'bot_username': 'Stoneyard_Doge_Bot',
            'exchange': 'OKX',
            'trading_type': 'Spot'
        },

        'XRP_Spot_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS_XRP_SPOT_BINANCE,
            'bot_username': 'Stoneyard_XRP_Bot',
            'exchange': 'Binance',
            'trading_type': 'Spot'
        },
        
        
        # Perpetual Trading Bots
        'Doge_Perpetual_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS_DOGE_PERPETUAL_BINANCE,
            'bot_username': 'Stoneyard_Perpetual_Doge_Bot',
            'exchange': 'Binance',
            'trading_type': 'Perpetual'
        },
        'Doge_Perpetual_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS_DOGE_PERPETUAL_KUCOIN,
            'bot_username': 'Stoneyard_Perpetual_Doge_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Perpetual'
        },
        'Doge_Perpetual_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS_DOGE_PERPETUAL_OKX,
            'bot_username': 'Stoneyard_Perpetual_Doge_Bot',
            'exchange': 'OKX',
            'trading_type': 'Perpetual'
        },

        'XRP_Perpetual_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS_XRP_PERPETUAL_BINANCE,
            'bot_username': 'Stoneyard_Perpetual_XRP_Bot',
            'exchange': 'Binance',
            'trading_type': 'Perpetual'
        },
        
        # Add more bots as needed
    }

    # Logging Configuration
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'formatter': 'standard',
                'mode': 'a'
            }
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True
            },
            'blockchain_utils': {
                'level': 'DEBUG',
                'propagate': True
            }
        }
    }


    # API Endpoints
    API_ENDPOINTS = {
        'MARKET_DATA': 'https://api.coingecko.com/api/v3/coins/markets',
        'SIGNAL_ALERTS': 'https://api.cryptosignals.com/v1/signals'
    }

    @classmethod
    def get_bot_config(cls, bot_name: str) -> Dict[str, Any]:
        """
        Retrieve specific bot configuration
        
        Args:
            bot_name (str): Name of the bot
        
        Returns:
            Dict containing bot configuration
        """
        return cls.BOT_PAYMENT_CONFIGS.get(bot_name, {})

    @classmethod
    def validate_bot_config(cls, bot_name: str) -> bool:
        """
        Validate if bot configuration exists
        
        Args:
            bot_name (str): Name of the bot
        
        Returns:
            bool: Whether bot configuration is valid
        """
        return bot_name in cls.BOT_PAYMENT_CONFIGS

# Logging Configuration
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s - RPC URL: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': 'app.log',
                'formatter': 'standard',
                'mode': 'a'
            }
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True
            },
            'blockchain_utils': {
                'level': 'DEBUG',
                'propagate': True
            }
        }
    }

    # RPC URL
    RPC_URL = os.getenv('RPC_URL')

    @classmethod
    def setup_logging(cls):
        import logging.config
        logging.config.dictConfig(cls.LOGGING_CONFIG)
        logger = logging.getLogger(__name__)
        logger.info(f"RPC URL configured: {cls.RPC_URL}")

    def __repr__(self):
        return f"<PrivateNess Network Configuration>"
    