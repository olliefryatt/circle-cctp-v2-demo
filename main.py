import time
from burn_v2 import burn_usdc
from eth_balance import check_eth_and_usdc_balance
from get_attestation import fetch_attestation
from mint_on_base import mint_usdc

# ETH - USDC - balance = $3  (now $1)
# BASE - USDC - balance = $3

# Configurable flag: set to True to wait & see entire flow, False to skip attestation & use a previsouly produced/approved tx hash
WAIT_FOR_APPROVAL = True

# Manual burn tx hash to use if skipping wait (put your known & approved tx hash here)
MANUAL_BURN_TX_HASH = "75fb37490e284dae7a4bc487cff14f5be52660e236d2efa376e2cbc71c7325ac" 
# af71fdb78bb68b43e66584551a88add7a8e3a6a251201285d8a4c365b8ba3b90

def wait_for_circle_approval(wait_minutes=10, update_interval=30):
    # This function waits for Circle to process the burn and produce attestation
    total_seconds = wait_minutes * 60
    elapsed = 0
    print(f"\n⏳ Waiting for Circle attestation to be ready (~{wait_minutes} minutes)...")
    while elapsed < total_seconds:
        mins_left = (total_seconds - elapsed) // 60
        secs_left = (total_seconds - elapsed) % 60
        print(f"  ⏰ Time remaining: {mins_left} min {secs_left} sec", end="\r", flush=True)
        time.sleep(update_interval)
        elapsed += update_interval
    print("\n✅ Wait complete! Proceeding to fetch attestation...\n")

def main():

    # STEP 1: Check balances on Ethereum Sepolia before burning
    print("\n=== Step 1: Checking wallet balances on Ethereum Sepolia ===")
    balances = check_eth_and_usdc_balance()

    # STEP 2: Check if script should wait for Circle approval or use manual tx hash
    print("\n=== Step 2: Starting Circle CCTP Burn Flow ===\n")

    if WAIT_FOR_APPROVAL:
        burn_tx_hash = burn_usdc()
        print("Done producing burn TX hash")

        wait_for_circle_approval(wait_minutes=10, update_interval=30)
    else:
        burn_tx_hash = MANUAL_BURN_TX_HASH
        print(f"\n⏳ Skipping burn & waiting for attestation. Using a TX hash produced previously:\n{burn_tx_hash}\n")

    # STEP 3: Save the burn_tx_hash (whether from burn or manual) for get_attestation.py to read
    print("=== Step 3: Saving burn_tx_hash.txt ===")
    print(" ")
    with open("burn_tx_hash.txt", "w") as f:
        f.write(burn_tx_hash)

    # STEP 4: Fetch the attestation and message from Circle API 
    print("=== Step 4: Fetching attestation and message from Circle ===")
    message, attestation = fetch_attestation()
    print("✅ Ready for minting on Base Sepolia.")
    print(" ")

    # STEP 5: Mint USDC on Base Sepolia
    print("=== Step 5: Minting USDC on Base Sepolia ===")
    print(" ")
    mint_tx_hash = mint_usdc()
    print(f"\n✅ Mint transaction sent. TX hash:\n{mint_tx_hash}\n")
    print(" ")

    # STEP 6: Check balances on Base Sepolia & Ethereum Sepolia after minting
    print("=== Step 6: Checking balances on Base Sepolia & Ethereum Sepolia after minting ===")
    print(" ")
    balances = check_eth_and_usdc_balance()
    print(" ")


if __name__ == "__main__":
    main()
