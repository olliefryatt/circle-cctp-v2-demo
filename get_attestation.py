import requests
import json
import time

def fetch_attestation(poll_interval=10, max_attempts=60):
    with open("burn_tx_hash.txt", "r") as f:
        burn_tx_hash = f.read().strip()
    if not burn_tx_hash.startswith("0x"):
        burn_tx_hash = "0x" + burn_tx_hash

    source_domain_id = 0  # Sepolia
    url = f"https://iris-api-sandbox.circle.com/v2/messages/{source_domain_id}?transactionHash={burn_tx_hash}"

    print("="*60)
    print(f"🔎 Fetching attestation and message for TX:\n  {burn_tx_hash}\nfrom:\n  {url}")
    print("="*60)

    attempt = 0
    while attempt < max_attempts:
        response = requests.get(url)
        data = response.json()

        if "messages" in data and data["messages"]:
            msg = data["messages"][0]
            status = msg.get("status", "unknown")
            print(f"Attempt {attempt + 1}: Message status = {status}")

            if status == "complete":
                attestation = msg.get("attestation")
                message = msg.get("message")

                with open("attestation.txt", "w") as af:
                    af.write(attestation)
                with open("message.txt", "w") as mf:
                    mf.write(message)

                print(f"✅ Attestation and message saved to files.")
                if msg.get("decodedMessage"):
                    print("🔍 Decoded Message:")
                    print(json.dumps(msg["decodedMessage"], indent=2))
                return message, attestation

            elif status in ["pending", "pending_confirmations"]:
                if msg.get("delayReason"):
                    print(f"⏳ Delay reason: {msg['delayReason']}")
                print(f"Waiting {poll_interval} seconds before retrying...\n")
                time.sleep(poll_interval)
            else:
                print(f"Unexpected status '{status}', exiting.")
                break
        else:
            print("❌ No message found yet for this transaction hash.")
            time.sleep(poll_interval)
        attempt += 1

    raise TimeoutError("Attestation not ready after maximum attempts.")

# For standalone test run:
if __name__ == "__main__":
    fetch_attestation()
