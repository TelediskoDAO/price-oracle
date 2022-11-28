#!/usr/bin/env python3
from web3 import Web3
from eth_utils.address import to_checksum_address
from eth_account import Account
from contract import ABI
from price import get
import time
import os
import schedule

ORACLE = to_checksum_address(os.environ["ORACLE"])
PRIVATE_KEY = os.environ["PRIVATE_KEY"]
PROVIDER_URL = os.environ.get("PROVIDER_URL", "http://127.0.0.1:8545")
CHAIN_ID = int(os.environ.get("CHAIN_ID", "666666"))
FREQUENCY = int(os.environ.get("FREQUENCY", "1"))


def run():
  w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

  if not w3.isConnected():
    exit("Not connected")

  SYMBOLS = ["EEUR", "EUR"]
  prices = []
  for symbol in SYMBOLS:
    prices.append(int(get(symbol) * 1e9))
  times = [int(time.time())] * 2

  oracle_contract = w3.eth.contract(address=ORACLE, abi=ABI)
  account = Account.from_key(PRIVATE_KEY)
  nonce = w3.eth.getTransactionCount(account.address)

  max_fee = 25
  max_priority_fee = 2

  print(f"""\
    submitting\n\
      symbols: {SYMBOLS}\n\
      prices: {prices}\n\
      times: {times}\n\
  """)

  relay_txn = oracle_contract.functions.relay(SYMBOLS, prices, times).buildTransaction({
      'chainId': CHAIN_ID,
      'maxFeePerGas': Web3.toWei(max_fee, 'gwei'),
      'maxPriorityFeePerGas': Web3.toWei(max_priority_fee, 'gwei'),
      'from': account.address,
      'nonce': nonce
  })

  signed_txn = w3.eth.account.signTransaction(relay_txn, private_key=PRIVATE_KEY)
  tx_hash = w3.toHex(w3.keccak(signed_txn.rawTransaction))
  w3.eth.sendRawTransaction(signed_txn.rawTransaction)
  print(tx_hash)



schedule.every(FREQUENCY).minutes.do(run)

while True:
    schedule.run_pending()
    time.sleep(1)