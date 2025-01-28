import os
from dotenv import load_dotenv
import requests
import logging
from typing import Dict, Any
from datetime import datetime, timedelta
from utils.config import Config
# Load environment variables from .env file
load_dotenv()

class PrivatenessBlockchainClient:
    def __init__(self, rpc_url: str = None):
        # Create a logger for this class
        self.logger = logging.getLogger(__name__)
        # Set the RPC URL, defaulting to a local address if not provided
        self.rpc_url = rpc_url or os.getenv('RPC_URL', 'http://127.0.0.1:6660')  # Default RPC URL with /wallets

        # Log RPC URL for debugging
        self.logger.info(f"Initializing BlockchainClient with RPC URL: {self.rpc_url}")

    def make_rpc_request(self, method: str, params: list) -> Dict[str, Any]:
        """
        Make an RPC request to the blockchain node.

        Args:
            method (str): The RPC method to call.
            params (list): The parameters for the RPC method.

        Returns:
            dict: The response from the RPC call.
        """
        headers = {"Content-Type": "application/json"}
        data = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}

        try:
            response = requests.post(self.rpc_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"RPC request failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None

    def validate_transaction(self, tx_hash: str, required_amount: float) -> Dict[str, Any]:
        """
        Validate a transaction using the RPC interface.

        Args:
            tx_hash (str): The transaction hash to validate.
            required_amount (float): The required amount for the transaction.

        Returns:
            dict: A dictionary indicating whether the transaction is valid and any error messages.
        """
        try:
            # Construct the RPC request payload
            payload = {
                "jsonrpc": "2.0",
                "method": "validate_transaction",  # Ensure this is the correct method name
                "params": {
                    "tx_hash": tx_hash,
                    "required_amount": required_amount,
                    "payment_address": "2kGY2fECeGbaQWnq2QvZ9L7ng7QkerUraMn"  # Example payment address
                },
                "id": 1
            }

            # Send the RPC request
            response = requests.post(f'{self.rpc_url}/validate_transaction', json=payload)  # Ensure the correct endpoint
            response.raise_for_status()  # Raise an error for bad responses

            # Parse the response
            result = response.json()
            if 'error' in result:
                self.logger.error(f"RPC Error: {result['error']}")
                return {'valid': False, 'error': result['error']}
            return result['result']  # Adjust based on the actual response structure

        except Exception as e:
            self.logger.error(f"Transaction validation error: {e}")
            return {'valid': False, 'error': str(e)}

    def check_wallet_balance(self, address: str, minimum_ness: float) -> bool:
        """
        Check wallet balance via the RPC interface.

        Args:
            address (str): The wallet address to check.
            minimum_ness (float): The minimum NESS balance required.

        Returns:
            bool: True if the balance is sufficient, False otherwise.
        """
        try:
            # Construct the RPC request payload for checking balance
            payload = {
                "jsonrpc": "2.0",
                "method": "get_wallet_balance",  # Replace with the actual method name
                "params": {
                    "address": address
                },
                "id": 1
            }

            # Send the RPC request
            response = requests.post(self.rpc_url, json=payload)
            response.raise_for_status()  # Raise an error for bad responses

            # Parse the response
            result = response.json()
            if 'error' in result:
                self.logger.error(f"RPC Error: {result['error']}")
                return False
            
            # Check if the balance meets the minimum requirement
            balance = float(result.get('result', {}).get('ness_balance', 0))
            return balance >= minimum_ness

        except Exception as e:
            self.logger.error(f"Balance check error for {address}: {e}")
            return False