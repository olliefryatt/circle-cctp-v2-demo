import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
BASE_RPC_URL = os.getenv("BASE_RPC_URL")  # Base Sepolia endpoint

MT_ADDRESS = Web3.to_checksum_address("0xE737e5cEBEEBa77EFE34D4aa090756590b1CE275")

message_transmitter_abi = [
    {
        "inputs": [
            {"internalType": "bytes", "name": "message", "type": "bytes"},
            {"internalType": "bytes", "name": "attestation", "type": "bytes"}
        ],
        "name": "receiveMessage",
        "outputs": [
            {"internalType": "bool", "name": "", "type": "bool"}
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def mint_usdc():
    with open("message.txt", "r") as f:
        message = f.read().strip()
    with open("attestation.txt", "r") as f:
        attestation = f.read().strip()

    w3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))
    acct = w3.eth.account.from_key(PRIVATE_KEY)
    wallet_address = acct.address

    message_transmitter = w3.eth.contract(address=MT_ADDRESS, abi=message_transmitter_abi)

    print("="*60)
    print("About to mint USDC on Base Sepolia with the following parameters:")
    print(f"Message (truncated): {message[:20]}... (len {len(message)})")
    print(f"Attestation (truncated): {attestation[:20]}... (len {len(attestation)})")
    print("="*60)

    tx = message_transmitter.functions.receiveMessage(
        bytes.fromhex(message[2:]),  # Remove "0x"
        bytes.fromhex(attestation[2:])
    ).build_transaction({
        "from": wallet_address,
        "nonce": w3.eth.get_transaction_count(wallet_address),
        "gasPrice": w3.to_wei('5', 'gwei')
    })

    signed = acct.sign_transaction(tx)
    if hasattr(signed, 'rawTransaction'):
        tx_bytes = signed.rawTransaction
    elif hasattr(signed, 'raw_transaction'):
        tx_bytes = signed.raw_transaction
    else:
        tx_bytes = signed
    tx_hash = w3.eth.send_raw_transaction(tx_bytes)
    #print(f"✅ Mint TX sent! Hash: {tx_hash.hex()}")
    print("Check Base Sepolia explorer and your USDC balance after confirmation.")

    return tx_hash.hex()
