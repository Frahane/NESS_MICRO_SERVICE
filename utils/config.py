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
    DB_PATH = 'users.db'
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'
    WEBAPP_URL = os.getenv('WEBAPP_URL')
    
    

    # Database Configuration
    DB_PATH = os.getenv('DB_PATH')
    
    # Folder Configurations
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'

    # Blockchain Configuration
    PAYMENT_ADDRESS = "2kGY2fECeGbaQWnq2QvZ9L7ng7QkerUraMn"
    RPC_URL = os.getenv('RPC_URL')

    # Payment and Subscription Configuration
    SUBSCRIPTION_DURATION_DAYS = 30
    REQUIRED_NCH = 3000
    MINIMUM_NESS = 4000

    # Comprehensive Bot Payment Configurations
    BOT_PAYMENT_CONFIGS: Dict[str, Dict[str, Any]] = {
        # Spot Trading Bots
        'Doge_Spot_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Doge_Bot',
            'exchange': 'Binance',
            'trading_type': 'Spot'
        },
        'Doge_Spot_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Doge_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Spot'
        },
        'Doge_Spot_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Doge_Bot',
            'exchange': 'OKX',
            'trading_type': 'Spot'
        },

        'XRP_Spot_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_XRP_Bot',
            'exchange': 'Binance',
            'trading_type': 'Spot'
        },
        'XRP_Spot_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_XRP_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Spot'
        },
        'XRP_Spot_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_XRP_Bot',
            'exchange': 'OKX',
            'trading_type': 'Spot'
        },

        'ETH_Spot_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_ETH_Bot',
            'exchange': 'Binance',
            'trading_type': 'Spot'
        },
        'ETH_Spot_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_ETH_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Spot'
        },
        'ETH_Spot_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_ETH_Bot',
            'exchange': 'OKX',
            'trading_type': 'Spot'
        },

        'BTC_Spot_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_BTC_Bot',
            'exchange': 'Binance',
            'trading_type': 'Spot'
        },
        'BTC_Spot_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_BTC_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Spot'
        },
        'BTC_Spot_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_BTC_Bot',
            'exchange': 'OKX',
            'trading_type': 'Spot'
        },

        'SOL_Spot_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_SOL_Bot',
            'exchange': 'Binance',
            'trading_type': 'Spot'
        },
        'SOL_Spot_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_SOL_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Spot'
        },
        'SOL_Spot_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_SOL_Bot',
            'exchange': 'OKX',
            'trading_type': 'Spot'
        },

        'AVAX_Spot_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_AVAX_Bot',
            'exchange': 'Binance',
            'trading_type': 'Spot'
        },
        'AVAX_Spot_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_AVAX_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Spot'
        },
        'AVAX_Spot_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_AVAX_Bot',
            'exchange': 'OKX',
            'trading_type': 'Spot'
        },
        
        # Perpetual Trading Bots
        'Doge_Perpetual_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_Doge_Bot',
            'exchange': 'Binance',
            'trading_type': 'Perpetual'
        },
        'Doge_Perpetual_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_Doge_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Perpetual'
        },
        'Doge_Perpetual_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_Doge_Bot',
            'exchange': 'OKX',
            'trading_type': 'Perpetual'
        },

        'XRP_Perpetual_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_XRP_Bot',
            'exchange': 'Binance',
            'trading_type': 'Perpetual'
        },
        'XRP_Perpetual_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_XRP_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Perpetual'
        },
        'XRP_Perpetual_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_XRP_Bot',
            'exchange': 'OKX',
            'trading_type': 'Perpetual'
        },

        'ETH_Perpetual_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_ETH_Bot',
            'exchange': 'Binance',
            'trading_type': 'Perpetual'
        },
        'ETH_Perpetual_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_ETH_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Perpetual'
        },
        'ETH_Perpetual_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_ETH_Bot',
            'exchange': 'OKX',
            'trading_type': 'Perpetual'
        },

        'BTC_Perpetual_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_BTC_Bot',
            'exchange': 'Binance',
            'trading_type': 'Perpetual'
        },
        'BTC_Perpetual_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_BTC_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Perpetual'
        },
        'BTC_Perpetual_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_BTC_Bot',
            'exchange': 'OKX',
            'trading_type': 'Perpetual'
        },

        'SOL_Perpetual_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_SOL_Bot',
            'exchange': 'Binance',
            'trading_type': 'Perpetual'
        },
        'SOL_Perpetual_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_SOL_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Perpetual'
        },
        'SOL_Perpetual_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_SOL_Bot',
            'exchange': 'OKX',
            'trading_type': 'Perpetual'
        },

        'AVAX_Perpetual_Binance': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_AVAX_Bot',
            'exchange': 'Binance',
            'trading_type': 'Perpetual'
        },
        'AVAX_Perpetual_Kucoin': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_AVAX_Bot',
            'exchange': 'Kucoin',
            'trading_type': 'Perpetual'
        },
        'AVAX_Perpetual_OKX': {
            'required_nch': REQUIRED_NCH,
            'minimum_ness': MINIMUM_NESS,
            'payment_address': PAYMENT_ADDRESS,
            'bot_username': 'Stoneyard_Perpetual_AVAX_Bot',
            'exchange': 'OKX',
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
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
            },
            'file_handler': {
                'level': 'ERROR',
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': 'error.log',
                'mode': 'a',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['default', 'file_handler'],
                'level': 'INFO',
                'propagate': True
            },
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
        """
        Configure logging based on the defined configuration
        """
        import logging.config
        logging.config.dictConfig(cls.LOGGING_CONFIG)
        
        # Log RPC URL for debugging
        logger = logging.getLogger(__name__)
        logger.info(f"RPC URL configured: {cls.RPC_URL}")
    def __repr__(self):
        return f"<PrivateNess Network Configuration>"
    
