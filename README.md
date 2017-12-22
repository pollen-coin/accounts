# pollen_access [![Build Status](https://travis-ci.org/pollen-coin/pollen_access.svg?branch=master)](https://travis-ci.org/pollen-coin/pollen_access)
Python interface for Pollen and other cryptonote based currencies.

## Features:
- Payment IDs with custom notes of up to 20 characters
- Complete interface for wallet RPC including: sending transactions, checking balances, viewing incoming transactions
- Tested compatibility with Django and Flask

## Instructions
Installing:

`pip install pollen_access`

To start the RPC server:

- Run the Pollen node: `pollend`

- In a different terminal, create a wallet: `simplewallet`, follow the prompts, then type `exit`

- Start the RPC server with the wallet name and password you just created: `simplewallet --wallet-file=rpcWallet --password=password --rpc-bind-port=51515`

Use:

`from pollen_access import wallet`

`w = wallet.Wallet('ADDRESS', 'localhost', '51515')`

`balance = w.get_available_balance()`

`payment_id = w.generate_payment_id('Thanks for the fish')`

`tx_hash = w.transfer(self, 100, 'SENDADDRESS', payment_id, mixin=4)`