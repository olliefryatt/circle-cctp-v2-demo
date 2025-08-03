# base_balance.py

import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

def check_base_balances():
    BASE_RPC_URL = os.getenv("BASE_RPC_URL")

    USDC_BASE = Web3.to_checksum_address("0x26dF8d79C4FaCa88d0212f0bd7C4A4d1e8955F0e")

    w3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))

    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    if "WALLET_ADDRESS" in os.environ:
        wallet_address = Web3.to_checksum_address(os.getenv("WALLET_ADDRESS"))
    else:
        acct = w3.eth.account.from_key(PRIVATE_KEY)
        wallet_address = acct.address

    print(f"\nChecking balances for {wallet_address} on Base Sepolia...\n")

    # ETH balance
    eth_balance = w3.eth.get_balance(wallet_address)
    print(f"ETH balance: {w3.from_wei(eth_balance, 'ether')} ETH")

    # USDC balance (ERC20)
    usdc_abi = [{
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }]
    usdc = w3.eth.contract(address=USDC_BASE, abi=usdc_abi)

    try:
        usdc_balance = usdc.functions.balanceOf(wallet_address).call()
        print(f"USDC balance: {usdc_balance / 1e6} USDC (on Base Sepolia)")
    except Exception as e:
        print("Error querying USDC balance:", e)
