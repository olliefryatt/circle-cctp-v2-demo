# Circle CCTP Cross-Chain Transfer Demo

This project explores Circle’s CCTP v2 by bridging USDC from Ethereum Sepolia testnet to Base Sepolia testnet. It does not cover advanced features such as immediate transfers that bypass waiting for the attestation API (this can take 10min+) or the use of hooks. To understand this additional functionality please refer to Circle’s official documentation.

## Key Steps (see main.py)

This project follows the end-to-end Circle CCTP v2 flow to bridge USDC from Ethereum Sepolia testnet to Base Sepolia testnet. Below are the key steps with example transaction references you can see a actual on-chain (testnet) flow.

- **Step 1: Check ETH and USDC balances on Ethereum & Base Sepolia (testnet)**  

- **Step 2: Burn USDC on Ethereum Sepolia to initiate CCTP v2 cross-chain transfer**  
  This burns USDC on Sepolia and creates the cross-chain message.  
  Example burn TX hash: [`0xaf71fdb78bb68b43e66584551a88add7a8e3a6a251201285d8a4c365b8ba3b90`](https://sepolia.etherscan.io/tx/0xaf71fdb78bb68b43e66584551a88add7a8e3a6a251201285d8a4c365b8ba3b90)

- **Step 3: Wait for Circle to process the burn and generate attestation**  
  Circle requires about 15 minutes to finalize and sign the message. This script waits or you can skip wait and supply a known tx hash. You can also check this manually by using Circle’s Playground (insert TX hash from step 2 in the link below).

- **Step 4: Fetch attestation and message from Circle’s API**  
  Poll Circle’s API to retrieve the cryptographic proof and message needed for minting USDC on base. Again you can see this proof on Circle’s Playground (insert TX hash from step 2 in the link below)

- **Step 5: Mint USDC on Base Sepolia using the attestation and message**  
  The mint transaction creates equivalent USDC on Base Sepolia.  
  Example mint TX hash: [`0x99457161075087c7609e5c74788b63f7d88e92655f55dad9431c8f4ae8088378`](https://sepolia.basescan.org/tx/0x99457161075087c7609e5c74788b63f7d88e92655f55dad9431c8f4ae8088378)

- **Step 6: Verify USDC balances on Base Sepolia after mint**  
  Confirm that your USDC balance on Base Sepolia has increased as expected. And USDC balance on Ethereum Sepolia has decreased as expected.

## Useful Faucets

- [Circle Faucet](https://faucet.circle.com/)  
  *Sends testnet USDC to Ethereum Sepolia*

- [Alchemy Ethereum Sepolia Faucet](https://www.alchemy.com/faucets/ethereum-sepolia)  
  *Get Ethereum Sepolia testnet ETH*

- [Alchemy Base Sepolia Faucet](https://www.alchemy.com/faucets/base-sepolia)  
  *Get Base Sepolia testnet ETH*

## Key Docs & References

- [CCTP Documentation](https://developers.circle.com/cctp)
- [All Mainnet and Testnet Smart Contracts](https://developers.circle.com/cctp/evm-smart-contracts)
- [Contract ABIs (e.g., latest ABI for `TokenMessengerV2`)](https://github.com/circlefin/evm-cctp-contracts/blob/63ab1f0ac06ce0793c0bbfbb8d09816bc211386d/src/v2/TokenMessengerV2.sol#L158)
- [Circle’s Playground Attestation Service](https://developers.circle.com/api-reference/cctp/all/get-messages-v-2)  
  *Enter a burn `tx_hash` to check the request status*
