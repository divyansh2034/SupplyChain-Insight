from web3 import Web3
import json
import os
from dotenv import load_dotenv
from eth_account import Account
import eth_utils

class BlockchainHandler:
    def __init__(self):
        load_dotenv()
        
        # Connect to local blockchain
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('RPC_URL')))
        
        # Load contract ABI
        with open('build/contracts/SupplyChain.json', 'r') as f:
            contract_json = json.load(f)
            self.contract_abi = contract_json['abi']
        
        # Initialize contract
        self.contract_address = os.getenv('CONTRACT_ADDRESS')
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.contract_address),
            abi=self.contract_abi
        )
        
        # Set default account
        self.account_address = Web3.to_checksum_address(os.getenv('ACCOUNT_ADDRESS'))
        
        # Set up account with private key
        private_key = os.getenv('PRIVATE_KEY')
        if not private_key.startswith('0x'):
            private_key = '0x' + private_key
        self.account = Account.from_key(private_key)
        
    def add_product(self, name, origin, destination, scheduled_days, order_total):
        """Add a new product to the blockchain"""
        try:
            # Get nonce
            nonce = self.w3.eth.get_transaction_count(self.account_address)
            
            # Build transaction
            transaction = self.contract.functions.addProduct(
                name,
                origin,
                destination,
                scheduled_days,
                order_total
            ).build_transaction({
                'chainId': 1337,  # Ganache chain ID
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
                'from': self.account_address
            })
            
            # Sign transaction
            signed = self.account.sign_transaction(transaction)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
            print(f"Transaction sent! Hash: {tx_hash.hex()}")
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt
            
        except Exception as e:
            print(f"Error adding product: {e}")
            raise
            
    def get_product(self, product_id):
        """Get product details from blockchain"""
        try:
            return self.contract.functions.getProduct(product_id).call()
        except Exception as e:
            print(f"Error getting product: {e}")
            return None

    def check_connection(self):
        """Check if connected to blockchain"""
        try:
            connected = self.w3.is_connected()
            chain_id = self.w3.eth.chain_id
            balance = self.w3.eth.get_balance(self.account_address)
            
            print(f"Connected: {connected}")
            print(f"Chain ID: {chain_id}")
            print(f"Account Balance: {Web3.from_wei(balance, 'ether')} ETH")
            print(f"Using Account: {self.account_address}")
            
            return connected
        except Exception as e:
            print(f"Connection error: {e}")
            return False 