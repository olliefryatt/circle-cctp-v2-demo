# eth_balance.py

import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

def check_eth_and_usdc_balance():
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    RPC_URL = os.getenv("RPC_URL")

    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    if not w3.is_connected():
        print("❌ Could not connect to Sepolia RPC.")
        return None

    print(" ")
    print("✅ Connected to Sepolia RPC & checking balances on Ethereum Sepolia")

    acct = w3.eth.account.from_key(PRIVATE_KEY)
    wallet_address = acct.address
    print(f"Your wallet address: {wallet_address}")

    # Get ETH balance
    balance = w3.eth.get_balance(wallet_address)
    eth_balance = w3.from_wei(balance, 'ether')
    print(f"Sepolia ETH balance: {eth_balance} ETH")

    # Check USDC balance
    USDC_ADDRESS = Web3.to_checksum_address("0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238")
    usdc_abi = [{
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }]
    usdc = w3.eth.contract(address=USDC_ADDRESS, abi=usdc_abi)
    usdc_balance = usdc.functions.balanceOf(wallet_address).call()
    print(f"USDC testnet balance: {usdc_balance / 1e6} USDC")
    print(" ")
    return eth_balance, usdc_balance / 1e6
