import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")

# Faucet
# USDC https://faucet.circle.com/ 
# ETH https://sepoliafaucet.com/
# https://sepolia.etherscan.io/address/0x29c04ABCFc1F2b43Ac3400a45Ca291004A2b903A

# Constants
USDC_ADDRESS = Web3.to_checksum_address("0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238")
TOKEN_MESSENGER = Web3.to_checksum_address("0x8FE6B999Dc680CcFDD5Bf7EB0974218be2542DAA")
DEST_DOMAIN = 6  
# Base Sepolia (not the same as chain ID; it’s an internal mapping used by CCTP.)
# Note Base Sepolia --> 6 https://developers.circle.com/cctp/evm-smart-contracts

def burn_usdc(amount=1 * 10**6):
    # Setup web3
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    acct = w3.eth.account.from_key(PRIVATE_KEY)
    wallet_address = acct.address

    # USDC ABI: just the approve function
    usdc_abi = [
        {
            "name": "approve",
            "type": "function",
            "inputs": [
                {"name": "spender", "type": "address"},
                {"name": "value", "type": "uint256"},
            ],
            "outputs": [{"type": "bool"}],
            "stateMutability": "nonpayable",
        }
    ]

    # TokenMessenger ABI: just the depositForBurn function
    messenger_abi = [
        {
            "inputs": [
                {"internalType": "uint256", "name": "amount", "type": "uint256"},
                {"internalType": "uint32",  "name": "destinationDomain", "type": "uint32"},
                {"internalType": "bytes32", "name": "mintRecipient", "type": "bytes32"},
                {"internalType": "address", "name": "burnToken", "type": "address"},
                {"internalType": "bytes32", "name": "destinationCaller", "type": "bytes32"},
                {"internalType": "uint256", "name": "maxFee", "type": "uint256"},
                {"internalType": "uint32", "name": "minFinalityThreshold", "type": "uint32"},
            ],
            "name": "depositForBurn",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]

    # Load contracts
    usdc = w3.eth.contract(address=USDC_ADDRESS, abi=usdc_abi)
    messenger = w3.eth.contract(address=TOKEN_MESSENGER, abi=messenger_abi)

    # Amount to burn: 1 USDC = 1 * 10^6
    amount = 1 * 10**6


    # Step 0: Start
    print("Okay starting burning of USDC...")

    # Get current nonce once
    nonce = w3.eth.get_transaction_count(wallet_address)

    # STEP 1: Approve
    # This gives the CCTP contract permission to move (burn) my USDC.
    print("Approving USDC for TokenMessenger...")
    approve_txn = usdc.functions.approve(TOKEN_MESSENGER, amount).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 80000,
        'gasPrice': w3.to_wei('5', 'gwei')
    })
    signed_approve = acct.sign_transaction(approve_txn)
    tx_hash = w3.eth.send_raw_transaction(signed_approve.rawTransaction if hasattr(signed_approve, "rawTransaction") else signed_approve.raw_transaction if hasattr(signed_approve, "raw_transaction") else signed_approve)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("✅ Approved. TX hash:", tx_hash.hex())

    # Increment nonce for next tx
    nonce += 1

    # STEP 2: Burn
    # This actually burns my USDC, emits a DepositForBurn event, and signals to CCTP that I want to transfer to another chain
    print("Calling depositForBurn...")
    recipient_bytes32 = w3.to_bytes(hexstr=wallet_address).rjust(32, b'\0')
    zero_bytes32 = b'\x00' * 32
    max_fee = 0 # w3.to_wei("0.0001", "ether")
    min_finality_threshold = 0
    burn_txn = messenger.functions.depositForBurn(
        amount,
        DEST_DOMAIN,
        recipient_bytes32,
        USDC_ADDRESS,
        zero_bytes32,
        max_fee,
        min_finality_threshold
    ).build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gasPrice': w3.to_wei('5', 'gwei')
        # let web3.py estimate gas
    })
    signed_burn = acct.sign_transaction(burn_txn)
    if hasattr(signed_burn, 'rawTransaction'):
        burn_tx_bytes = signed_burn.rawTransaction
    elif hasattr(signed_burn, 'raw_transaction'):
        burn_tx_bytes = signed_burn.raw_transaction
    else:
        burn_tx_bytes = signed_burn
    burn_tx_hash = w3.eth.send_raw_transaction(burn_tx_bytes)
    burn_receipt = w3.eth.wait_for_transaction_receipt(burn_tx_hash)
    print("🔥 Burn complete. TX hash:", burn_tx_hash.hex())

    # STEP 3: Save the burn TX hash to a file
    with open("burn_tx_hash.txt", "w") as f:
        f.write(burn_tx_hash.hex())
    print("Burn TX hash saved to burn_tx_hash.txt")

    return burn_tx_hash.hex()

# If you want to test this module independently:
if __name__ == "__main__":
    burn_usdc()