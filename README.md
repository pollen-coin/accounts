# accounts
Python interface for Pollen and other cryptonote based currencies with account abstractions

To start the RPC server:

-Run the Pollen node: `pollend`

-In a different terminal, create a wallet: `simplewallet` then type `exit`

-Start the RPC server with the wallet name and password you just created: `simplewallet --wallet-file=rpcWallet --password=password --rpc-bind-port=51515`