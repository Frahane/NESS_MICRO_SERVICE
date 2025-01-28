import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from .blockchain_utils import PrivatenessBlockchainClient
from utils.config import Config
from utils.db_utils import (
    save_bot_subscription,
    get_user_bot_subscription,
    remove_bot_subscription,
)

logger = logging.getLogger(__name__)

class BotAccessManager:
    def __init__(self):
        self.blockchain_client = PrivatenessBlockchainClient()
        self.logger = logger

    def verify_bot_access(
        self,
        telegram_id: int,
        bot_name: str,
        tx_hash: str
    ) -> Dict[str, Any]:
        """
        Comprehensive bot access verification
        """
        # Retrieve bot-specific configuration
        bot_config = Config.BOT_PAYMENT_CONFIGS.get(bot_name)
        if not bot_config:
            return {
                'success': False,
                'message': f'Invalid bot: {bot_name}'
            }

        # Check if user already has an active subscription
        subscription = get_user_bot_subscription(telegram_id, bot_name)
        if subscription and subscription['expires_at'] > datetime.now():
            return {
                'success': True,
                'message': 'You already have an active subscription',
                'bot_username': bot_config['bot_username'],
                'payment_address': Config.PAYMENT_ADDRESS
            }

        # Validate transaction
        tx_validation = self.blockchain_client.validate_transaction(
            tx_hash,
            bot_config['required_nch']
        )

        if not tx_validation.get('valid'):
            return {
                'success': False,
                'message': 'Invalid transaction'
            }

        # Check paying address NESS balance
        paying_address = tx_validation.get('from_address')
        balance_valid = self.blockchain_client.check_wallet_balance(
            paying_address,
            bot_config['minimum_ness']
        )

        if not balance_valid:
            return {
                'success': False,
                'message': 'Insufficient NESS balance'
            }

        # Create and save subscription
        subscription = {
            'telegram_id': telegram_id,
            'bot_name': bot_name,
            'bot_username': bot_config['bot_username'],
            'payment_address': paying_address,
            'expires_at': datetime.now() + timedelta(days=Config.SUBSCRIPTION_DURATION_DAYS)
        }
        save_bot_subscription(subscription)

        return {
            'success': True,
            'message': 'Bot access granted',
            'bot_username': bot_config['bot_username'],
            'payment_address': Config.PAYMENT_ADDRESS
        }

    def check_ongoing_bot_access(
        self, 
        telegram_id: int, 
        bot_name: str
    ) -> Dict[str, Any]:
        """
        Check and maintain ongoing bot access
        """
        subscription = get_user_bot_subscription(telegram_id, bot_name)
        
        if not subscription:
            return {
                'access': False, 
                'message': 'No active subscription'
            }


    def check_subscription_status(self, telegram_id: int, bot_name: str) -> bool:
        """
        Check subscription status
        """
        subscription = get_user_bot_subscription(telegram_id, bot_name)
        if subscription and subscription['expires_at'] > datetime.now():
            # Check if user still holds the minimum NESS balance
            balance_valid = self.blockchain_client.check_wallet_balance(
                subscription['payment_address'],
                Config.MINIMUM_NESS
            )
            if not balance_valid:
                # Remove subscription if user fails to hold the minimum NESS balance
                remove_bot_subscription(telegram_id, bot_name)
                return False
            return True
        return False