import logging
from datetime import datetime, timedelta
from typing import Dict, Any
from utils.blockchain_utils import PrivatenessBlockchainClient
from utils.config import Config
from utils.db_utils import (
    save_bot_subscription,
    get_user_bot_subscription,
    remove_bot_subscription,
    log_fallback_usage,
)

logger = logging.getLogger(__name__)

class BotAccessManager:
    def __init__(self):
        self.blockchain_client = PrivatenessBlockchainClient()
        self.logger = logger

    def verify_bot_access(self, telegram_id: int, bot_name: str, tx_hash: str) -> Dict[str, Any]:
        """
        Verifies bot access by checking if a valid transaction has been made.
        If no subscription exists, it returns a response to trigger showPaymentModal().
        """
        bot_config = Config.BOT_PAYMENT_CONFIGS.get(bot_name)
        if not bot_config:
            return {'success': False, 'message': f'Invalid bot: {bot_name}'}

        # Check if user already has an active subscription
        subscription = get_user_bot_subscription(telegram_id, bot_name)
        if subscription and subscription['expires_at'] > datetime.now():
            return {
                'success': True,
                'message': 'You already have an active subscription',
                'bot_username': bot_config['bot_username'],
                'payment_address': bot_config['payment_address']  # ✅ Bot-specific address
            }

        # No active subscription, return response that triggers showPaymentModal()
        return {
            'success': False,
            'message': 'No active subscription. Please make the required payment.',
            'requires_payment': True,
            'payment_details': {
                'required_nch': bot_config['required_nch'],
                'minimum_ness': bot_config['minimum_ness'],
                'payment_address': bot_config['payment_address']  # ✅ Corrected here
            }
        }

    def verify_payment_transaction(self, telegram_id: int, bot_name: str, tx_hash: str) -> Dict[str, Any]:
        """
        Handles payment verification by checking transaction validity and NESS balance.
        Uses RPC first, falls back to Selenium if needed.
        """
        bot_config = Config.BOT_PAYMENT_CONFIGS.get(bot_name)
        if not bot_config:
            logger.error(f"[Verification] Invalid bot: {bot_name}")
            return {'success': False, 'message': f'Invalid bot: {bot_name}'}

        # Log received transaction
        logger.info(f"[VERIFICATION] Checking TX: {tx_hash} for bot {bot_name} by user {telegram_id}")

        # Validate transaction via RPC, fallback to Selenium if needed
        tx_validation = self.blockchain_client.validate_transaction(tx_hash, bot_config['required_nch'])
        
        if not tx_validation.get('valid'):
            log_fallback_usage(tx_hash, "Transaction Verification")
            logger.error(f"[VERIFICATION FAILED] TX: {tx_hash} | Reason: {tx_validation.get('error')}")
            print(f"[VERIFICATION FAILED] TX: {tx_hash} | Reason: {tx_validation.get('error')}")  # Debugging
            return {'success': False, 'message': 'Invalid transaction'}

        # Extracted transaction data
        nch_sent = tx_validation.get('nch_amount', 0)
        paying_address = tx_validation.get('from_address')

        logger.info(f"[VERIFICATION SUCCESS] TX: {tx_hash} | NCH Sent: {nch_sent}")
        print(f"[VERIFICATION SUCCESS] TX: {tx_hash} | NCH Sent: {nch_sent}")  # Debugging

        # ✅ Correct Validation: Check NCH Sent (Hours)
        if nch_sent < bot_config['required_nch']:
            logger.error(f"[VERIFICATION FAILED] TX: {tx_hash} | Sent {nch_sent} NCH, required {bot_config['required_nch']}")
            print(f"[VERIFICATION FAILED] TX: {tx_hash} | Sent {nch_sent} NCH, required {bot_config['required_nch']}")  # Debugging
            return {'success': False, 'message': f'Not enough NCH included: {nch_sent} (expected: {bot_config["required_nch"]})'}

        # ✅ Check sender's NESS balance in wallet (not transaction)
        balance_valid = self.blockchain_client.check_wallet_balance(paying_address, bot_config['minimum_ness'])
        if not balance_valid:
            log_fallback_usage(paying_address, "Balance Check")
            logger.error(f"[VERIFICATION FAILED] TX: {tx_hash} | Sender {paying_address} has insufficient balance")
            print(f"[VERIFICATION FAILED] TX: {tx_hash} | Sender {paying_address} has insufficient balance")  # Debugging
            return {'success': False, 'message': 'Insufficient NESS balance in wallet'}

        # ✅ Save the subscription (if all conditions met)
        subscription = {
            'telegram_id': telegram_id,
            'bot_name': bot_name,
            'bot_username': bot_config['bot_username'],
            'payment_address': paying_address,
            'expires_at': datetime.now() + timedelta(days=Config.SUBSCRIPTION_DURATION_DAYS)
        }
        save_bot_subscription(subscription)

        logger.info(f"[SUBSCRIPTION ACTIVATED] User: {telegram_id} | Bot: {bot_name} | TX: {tx_hash}")
        print(f"[SUBSCRIPTION ACTIVATED] User: {telegram_id} | Bot: {bot_name} | TX: {tx_hash}")  # Debugging
        
        return {
            'success': True,
            'message': 'Bot access granted',
            'bot_username': bot_config['bot_username'],
            'payment_address': bot_config['payment_address']
        }

    def check_ongoing_bot_access(self, telegram_id: int, bot_name: str) -> Dict[str, Any]:
        """
        Check and maintain ongoing bot access.
        If no subscription is found, trigger the payment modal.
        """
        subscription = get_user_bot_subscription(telegram_id, bot_name)
        if not subscription:
            return {'access': False, 'message': 'No active subscription'}

        return {'access': True, 'expires_at': subscription['expires_at']}

    def check_subscription_status(self, telegram_id: int, bot_name: str) -> bool:
        """
        Checks if a user's subscription is still valid.
        """
        subscription = get_user_bot_subscription(telegram_id, bot_name)
        if subscription and subscription['expires_at'] > datetime.now():
            balance_valid = self.blockchain_client.check_wallet_balance(
                subscription['payment_address'], Config.MINIMUM_NESS
            )
            if not balance_valid:
                remove_bot_subscription(telegram_id, bot_name)
                return False
            return True
        return False