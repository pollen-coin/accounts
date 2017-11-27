import json
import os
import binascii
import configparser
import requests

class WalletException(Exception):
    """Raised for exceptions related to the Pollen Wallet"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Wallet:
    """
    Implementation of Pollen rpc api
    """

    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read('config.ini')
        self.config = self.config_parser['wallet']
        self.address = self.config['address']
        self.rpc_host = self.config['rpc_host']
        self.rpc_port = self.config['rpc_port']
        self.rpc_url = self.rpc_host + ':' + self.rpc_port + '/json_rpc'

    def post_request(self, method, params=None):
        headers = {'content-type': 'application/json'}

        if params is None:
            data = {
                "method": method
            }
        else:
            data = {
                "method": method,
                "params": params
            }

        data.update({"jsonrpc": "2.0", "id": "0"})

        response = requests.post(
            self.rpc_url,
            data=json.dumps(data),
            headers=headers,
        )

        response_data = response.json()

        if 'error' in response_data:
            if 'message' in response_data['error']:
                raise WalletException(response_data['error']['message'])
            else:
                raise WalletException('Unspecified RPC Error')

        return response_data

    def get_address(self):
        """
        :return: wallet's address
        """
        return self.address

    def get_unverified_balance(self):
        """
        :return: unconfirmed balance of the wallet
        """
        rpc_method = 'getbalance'
        result = self.post_request(rpc_method)['result']
        unverified_balance = result['locked_amount']
        float_amount = cryptonote_to_pollen(unverified_balance)
        return float_amount

    def get_available_balance(self):
        """
        :return: confirmed balance of the wallet
        """
        rpc_method = 'getbalance'
        result = self.post_request(rpc_method)['result']
        available_balance = result['available_balance']
        float_amount = cryptonote_to_pollen(available_balance)
        return float_amount

    def get_payment_info(self, payment_id):
        """
        :param payment_id:
        :return: List of payments with matching Payment ID
        [{'tx_hash': 'f6116e04b87551bbc4b0f1ab8fa41494d0a9f83815c9a98eae7113087bc0aa29', 'amount': 100,
         'block_height': 1339, 'unlock_time': 0}]
        """
        rpc_method = 'get_payments'
        params = {"payment_id": payment_id,}
        result = self.post_request(rpc_method, params)['result']
        payments = result['payments']

        # Convert amounts to Pollen
        for payment in payments:
            payment['amount'] = cryptonote_to_pollen(payment['amount'])

        return payments

    def get_transfers(self):
        """
        :return: List of all wallet transfers.
        Example:
        [{"address":"","amount":102,"blockIndex":1174,"fee":0,"output":false,"paymentId":"","time":1511816829,
          "transactionHash":"76ab7ce1a049d6bc3e35cebee6acc17b6861326ac8749188c422ca05dc1ced2a","unlockTime":1334},
        ...]
        """
        rpc_method = 'get_transfers'
        result = self.post_request(rpc_method)['result']
        transfers = result['transfers']

        # Convert amounts to Pollen
        for transfer in transfers:
            transfer['amount'] = cryptonote_to_pollen(transfer['amount'])

        return transfers

    def transfer(self, amount, deposit_address, payment_id, mixin=1):
        """
        :param amount: The amount to transfer.
        :param deposit_address: The address to which coin will be sent.
        :param payment_id: The payment id to include in the transaction.
        :param mixin: The mixin count to use.  Defaults to 4.
        :return: The transaction hash.
        """
        rpc_method = 'transfer'

        # TODO: Sanity check on conversion
        cryptonote_amount = pollen_to_cryptonote(amount)

        recipients = [{"address": deposit_address,
                       "amount": cryptonote_amount}]

        params = {"destinations": recipients,
                  "mixin": mixin,
                  "payment_id": payment_id}

        result = self.post_request(rpc_method, params)['result']
        tx_hash = result['tx_hash']

        return tx_hash

    def has_rpc_access(self):
        """
        :return: True if no connection error
        """
        try:
            self.get_transfers()
        except requests.ConnectionError:
            return False
        return True

    def all_deposits_confirmed(self):
        return self.get_available_balance() == self.get_unverified_balance()


def cryptonote_to_pollen(cryptonote_amount):
    """
    :param cryptonote_amount: String
    :return: float amount in Pollen
    """
    cryptonote_amount = str(cryptonote_amount)
    if len(cryptonote_amount) < 13:
        cryptonote_amount = '0' * (13 - len(cryptonote_amount)) + cryptonote_amount
    point_index = len(cryptonote_amount) - 13
    float_string = cryptonote_amount[0:point_index] + "." + cryptonote_amount[point_index:]
    float_amount = float(float_string)
    return float_amount


def pollen_to_cryptonote(float_amount):
    """
    :param float_amount: Pollen amount
    :return: CryptoNote integer
    """
    float_string = str(float_amount)
    power_accumulator = 0

    if '.' in float_string:
        point_index = float_string.index('.')
        power_accumulator = len(float_string) - point_index - 1
        while power_accumulator < 13 and '0' == float_string[-1]:
            float_string = float_string[:-1]
            power_accumulator -= 1
        if power_accumulator > 13:
            return False
        float_string = float_string[:point_index] + float_string[point_index + 1:]

    if not float_string:
        return False
    if power_accumulator < 13:
        float_string += '0' * (13 - power_accumulator)

    # while float_string[0] == '0':
    #    float_string = float_string[1:]

    return int(float_string)


def generate_payment_id():
    """
    Generates a random payment id.
    :return: 30 character hex string
    """
    return binascii.b2a_hex(os.urandom(32))
