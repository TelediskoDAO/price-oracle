#!/usr/bin/env python3
from web3 import Web3
from web3.auto import w3
from eth_utils.address import to_checksum_address
from eth_account import Account
from contract import ABI
from price import get
import time
import os
import schedule

ORACLE = to_checksum_address(os.environ["ORACLE"])
PRIVATE_KEY = os.environ["PRIVATE_KEY"]
CHAIN_ID = int(os.environ.get("CHAIN_ID", "666666"))
FREQUENCY = int(os.environ.get("FREQUENCY", "1"))


def run():
  try:
    if not w3.isConnected():
      raise Exception("Not connected")

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

    with open("info.log", "a") as file:
      file.write(f"{int(time.time())}\t{SYMBOLS}\t{prices}\t{times}\t{tx_hash}\n")
  except Exception as e:
    with open("error.log", "a") as file:
      file.write(str(e) + "\n")
      

schedule.every(FREQUENCY).minutes.do(run)
run()

while True:
    schedule.run_pending()
    time.sleep(1)