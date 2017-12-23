#wallet-rpc-test
#12-21-17 Alex Dai

from pollen_access import wallet

home_address = 'Pv8oDBDnpsbeMkHtsVwssL74rp5qyJVxFaYntCmBrZA9RiULsAwpfVMSY3cS5twH8eJ6XE5fH9w7CY9W6BMuxRmr2eyAPwaG1'
send_address = 'Pv8VH3Wu5yCfx3SHMUJfdj7z2b4RToSJgGCZvB3GVqmFKief9v8bFa2TfiGMDZ8qSNPL4qhHBsmQQWQmSstNDX9w2Hfz2mV13'

w = wallet.Wallet(home_address, 'http://localhost', '51515')

balance = w.get_available_balance()
print("Balance:", balance)

unverified_balance = w.get_unverified_balance()
print("unverified_balance:", unverified_balance)

payment_id = w.generate_payment_id('Thanks for the fish')
print('payment_id:', payment_id)


tx_hash = w.transfer(100, send_address, payment_id, mixin=0)

