import json
import configparser
import requests
from requests.auth import HTTPDigestAuth

class WalletException(Exception):
    """Raised for exceptions related to the Pollen Wallet"""

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Wallet:
    """
    Implementation of rpc api
    """

    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read('config.ini')
        self.config = self.config_parser['wallet']
        self.wallet_name = self.config['wallet_name']
        self.rpc_host = self.config['rpc_host']
        self.rpc_port = self.config['rpc_port']
        self.rpc_user = self.config['rpc_user']
        self.rpc_pass = self.config['rpc_pass']
        self.rpc_url = self.rpc_host + ':' + self.rpc_port + '/json_rpc'

    def post_request(self, method, params={}):
        headers = {'content-type': 'application/json'}

        if not params:
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
            auth=HTTPDigestAuth(self.rpc_user, self.rpc_pass))

        response_data = response.json()

        if 'error' in response_data:
            raise PollenWalletException(response_data['error']['message'])

        return response_data

    def get_address(self):
        rpc_method = 'getaddress'
        result = self.post_request(rpc_method)['result']
        address = result['address']
        return address

    def get_unverified_balance(self):
        rpc_method = 'getbalance'
        result = self.post_request(rpc_method)['result']
        unverified_balance = result['balance']
        # TODO: Sanity check on conversion
        float_amount = cryptonote_to_float(unverified_balance)
        return float_amount

    def get_available_balance(self):
        rpc_method = 'getbalance'
        result = self.post_request(rpc_method)['result']
        available_balance = result['unlocked_balance']
        # TODO: Sanity check on conversion
        float_amount = cryptonote_to_float(available_balance)
        return float_amount

    def get_payment_info(self, payment_id):
        rpc_method = 'get_payments'

        params = {"payment_id": payment_id,
                  }

        result = self.post_request(rpc_method, params)['result']

        return result

    def transfer(self, amount, deposit_address, payment_id, mixin=4):
        rpc_method = 'transfer'

        # TODO: Sanity check on conversion
        cryptonote_amount = float_to_cryptonote(amount)

        recipients = [{"address": deposit_address,
                       "amount": cryptonote_amount}]

        params = {"destinations": recipients,
                  "mixin": mixin,
                  "payment_id": payment_id}

        result = self.post_request(rpc_method, params)['result']
        tx_hash = result['tx_hash']

        return tx_hash

    def get_expected_transaction_fee(self):
        """
        Returns expected fee/transaction in XMR
        """
        # TODO: make this more accurate.. maybe look at previous transactions using the daemon rpc
        fee = 0.03
        return fee

    def has_rpc_access(self):
        try:
            self.get_address()
            self.get_available_balance()
            self.get_unverified_balance()
        except requests.ConnectionError:
            return False
        return True

    def all_deposits_confirmed(self):
        return self.get_available_balance() == self.get_unverified_balance()


def cryptonote_to_float(cryptonote_amount):
    cryptonote_amount = str(cryptonote_amount)
    if len(cryptonote_amount) < 12:
        cryptonote_amount = '0' * (12 - len(cryptonote_amount)) + cryptonote_amount
    point_index = len(cryptonote_amount) - 12
    float_string = cryptonote_amount[0:point_index] + "." + cryptonote_amount[point_index:]
    float_amount = float(float_string)
    return float_amount


def float_to_cryptonote(float_amount):
    float_string = str(float_amount)
    power_accumulator = 0

    if '.' in float_string:
        point_index = float_string.index('.')
        power_accumulator = len(float_string) - point_index - 1
        while power_accumulator < 12 and '0' == float_string[-1]:
            float_string = float_string[:-1]
            power_accumulator -= 1
        if power_accumulator > 12:
            return False
        float_string = float_string[:point_index] + float_string[point_index + 1:]

    if not float_string:
        return False
    if power_accumulator < 12:
        float_string += '0' * (12 - power_accumulator)

    # while float_string[0] == '0':
    #    float_string = float_string[1:]

    return int(float_string)
