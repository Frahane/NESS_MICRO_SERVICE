import os
import logging
import requests
from dotenv import load_dotenv
from typing import Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.config import Config

# Load environment variables
load_dotenv()

class PrivatenessBlockchainClient:
    def __init__(self, rpc_url: str = None):
        self.logger = logging.getLogger(__name__)
        self.rpc_url = rpc_url or Config.RPC_URL
        self.explorer_url = Config.EXPLORER_URL

        # ✅ Keep Headless Mode and SSL Fixes
        chrome_options = Options()
        #chrome_options.add_argument("--headless")  # ✅ Keep running in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # ✅ Fix SSL Errors
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Set up Chrome WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        self.logger.info(f"[CONFIG] RPC_URL: {self.rpc_url}")
        self.logger.info(f"[CONFIG] EXPLORER_URL: {self.explorer_url}")

    def validate_transaction(self, tx_hash: str, bot_name: str) -> Dict[str, Any]:
        """
        Validate a transaction using Selenium first, then fall back to RPC if needed.
        """
        bot_config = Config.get_bot_config(bot_name)  # ✅ Get bot-specific payment address
        if not bot_config:
            return {"valid": False, "error": "Invalid bot name"}

        required_nch = bot_config["required_nch"]
        payment_address = bot_config["payment_address"]  # ✅ Ensure we check against the correct bot's address

        self.logger.info(f"[VALIDATION] Checking TX: {tx_hash} via Selenium first")

        # Run Selenium FIRST
        result = self.scrape_transaction_details(tx_hash, required_nch, payment_address)

        if result.get("valid"):
            self.logger.info(f"[VALIDATION SUCCESS] TX: {tx_hash} verified via Selenium")
            return result

        # If Selenium fails, switch to RPC
        self.logger.warning(f"[VALIDATION] Selenium failed for TX: {tx_hash}. Switching to RPC fallback.")
        result = self.make_rpc_request("validate_transaction", [tx_hash, required_nch])

        if result and "result" in result:
            self.logger.info(f"[VALIDATION SUCCESS] TX: {tx_hash} verified via RPC")
            return result

        # If both fail, return error
        self.logger.error(f"[VALIDATION FAILED] TX: {tx_hash} could not be verified via Selenium or RPC.")
        return {"valid": False, "error": "Transaction verification failed"}

    def scrape_transaction_details(self, tx_hash: str, required_nch: int, payment_address: str) -> Dict[str, Any]:
        """
        Uses Selenium to scrape transaction details dynamically.
        Extracts sender, receiver, and NCH sent.
        """
        url = f"{self.explorer_url}/app/transaction/{tx_hash}"

        self.logger.info(f"[SCRAPING] Extracting TX: {tx_hash} from {url}")

        try:
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 30)

            # ✅ Wait for transaction status
            status_element = wait.until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/div/app-transaction-detail/div/div/div[1]/div"))
            )
            status = status_element.text.strip()

            # ✅ Extract Sender Address
            sender_element = wait.until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/div/app-transaction-detail/app-transaction-info/div/div[3]/div[1]/div[1]/div[2]/a"))
            )
            sender_address = sender_element.text.strip()

            # ✅ Extract Receiver Address
            receiver_element = wait.until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/div/app-transaction-detail/app-transaction-info/div/div[3]/div[1]/div[2]/div[2]/a"))
            )
            receiver = receiver_element.text.strip()

            # ✅ Extract NCH Sent (Hours)
            nch_element = wait.until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/div/app-transaction-detail/app-transaction-info/div/div[3]/div[1]/div[2]/div[2]/div[2]/div[2]"))
            )
            nch_sent = int(nch_element.text.replace(",", "").strip())  # Convert to integer after removing commas

            self.logger.info(f"[SCRAPING SUCCESS] TX: {tx_hash} | Status: {status} | NCH Sent: {nch_sent} | Sender: {sender_address} | Receiver: {receiver}")

            # ✅ Validate only NCH (Hours) and ensure it was sent to the correct bot's address
            if status == "Confirmed" and nch_sent >= required_nch and receiver == payment_address:
                return {
                    "valid": True,
                    "from_address": sender_address,  # Pass sender address for balance check
                    "nch_amount": nch_sent
                }

            return {"valid": False, "error": "Transaction does not meet required NCH conditions"}

        except Exception as e:
            self.logger.error(f"[SCRAPING FAILED] TX: {tx_hash} | Error: {e}")
            return {"valid": False, "error": "Explorer unreachable. Please try again later."}

    def scrape_wallet_balance(self, address: str, minimum_ness: float) -> bool:
        """
        Uses Selenium to scrape the sender's wallet balance dynamically.
        Ensures the sender's NESS holdings are >= minimum_ness.
        """
        url = f"{self.explorer_url}/app/address/{address}/1"

        self.logger.info(f"[SCRAPING BALANCE] Checking balance for: {address}")

        try:
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 10)

            # ✅ Extract the balance value
            balance_element = wait.until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/div/div/app-address-detail/div[1]/div/div[5]/div"))
            )
            balance_text = balance_element.text.strip()

            # ✅ Remove commas and "SKY" text
            balance_text = balance_text.replace(",", "").replace("SKY", "").strip()
            balance_value = float(balance_text)

            self.logger.info(f"[SCRAPING SUCCESS] Address: {address} | Balance: {balance_value} NESS")

            return balance_value >= minimum_ness

        except Exception as e:
            self.logger.error(f"[SCRAPING FAILED] Address: {address} | Error: {e}")
            return False

    def check_wallet_balance(self, address: str, minimum_ness: float) -> bool:
        """
        Checks if the sender's wallet has at least `minimum_ness`.
        Uses Selenium scraping.
        """
        self.logger.info(f"[BALANCE CHECK] Verifying NESS balance for: {address}")
        return self.scrape_wallet_balance(address, minimum_ness)

    def __del__(self):
        """
        Ensures Selenium WebDriver is properly closed when the instance is deleted.
        """
        self.driver.quit()  # ✅ Keep Selenium cleanup