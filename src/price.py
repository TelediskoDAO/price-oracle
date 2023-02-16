#!/usr/bin/env python3

from eth_utils.address import to_checksum_address
from contracts import ABI_CHAINLINK
from web3 import Web3
import sys
import os

CONTRACTS = {
    "EUR": to_checksum_address(os.environ["EUR_USD_CONTRACT"]),
    "USDC": to_checksum_address(os.environ["USDC_USD_CONTRACT"])
}
WEB3_PROVIDER = os.environ["MAINNET_PROVIDER_URI"]

def get(symbol):
    w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
    contract = w3.eth.contract(address=CONTRACTS[symbol], abi=ABI_CHAINLINK)
    decimals = contract.functions.decimals().call()
    response = contract.functions.latestRoundData().call()
    return float(response[1]) / (10 ** decimals)
    
if __name__ == "__main__":
    try:
        print(get(sys.argv[1]))
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)