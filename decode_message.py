from web3 import Web3

def bytes32_to_address_from_slice(b32_slice: bytes) -> str:
    return Web3.to_checksum_address("0x" + b32_slice[-20:].hex())

def decode_message(raw_hex):
    if raw_hex.startswith("0x"):
        raw_hex = raw_hex[2:]
    data = bytes.fromhex(raw_hex)

    version = int.from_bytes(data[0:4], "big")
    nonce = int.from_bytes(data[4:12], "big")
    source_domain = int.from_bytes(data[12:16], "big")
    sender = bytes32_to_address_from_slice(data[16:48])
    recipient = bytes32_to_address_from_slice(data[48:80])
    destination_caller = bytes32_to_address_from_slice(data[80:112])
    amount = int.from_bytes(data[112:144], "big")
    burn_token = bytes32_to_address_from_slice(data[144:176])
    mint_recipient = bytes32_to_address_from_slice(data[176:208])
    max_fee = int.from_bytes(data[208:240], "big")
    min_finality_threshold = int.from_bytes(data[240:244], "big")

    print(f"Version: {version}")
    print(f"Nonce: {nonce}")
    print(f"Source Domain ID: {source_domain}")
    print(f"Sender: {sender}")
    print(f"Recipient: {recipient}")
    print(f"Destination Caller: {destination_caller}")
    print(f"Amount: {amount} (smallest USDC units)")
    print(f"Burn Token Address: {burn_token}")
    print(f"Mint Recipient Address: {mint_recipient}")
    print(f"Max Fee: {max_fee}")
    print(f"Min Finality Threshold: {min_finality_threshold}")

# Replace this with your message hex string
raw_message = "0x0000000100000000000000065de57f6f894ff32ab04a3cb53334be26dc20bb3e01937f3c98dc05a355ea57830000000000000000000000008fe6b999dc680ccfdd5bf7eb0974218be2542daa0000000000000000000000008fe6b999dc680ccfdd5bf7eb0974218be2542daa000000000000000000000000000000000000000000000000000000000000000000000000000007d0000000010000000000000000000000001c7d4b196cb0c7b01d743fbc6116a902379c723800000000000000000000000029c04abcfc1b43ac3400a45ca291004a2b903a00000000000000000000000000000000000000000000000000000000000f424000000000000000000000000029c04abcfc1b43ac3400a45ca291004a2b903a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

decode_message(raw_message)
