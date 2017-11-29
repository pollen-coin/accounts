import unittest
import math
from wallet import pollen_to_cryptonote, cryptonote_to_pollen


class CurrencyExchangeTestCase(unittest.TestCase):
	"""
	Tests if Pollen to Cryptonote Conversions are correct
	"""
	def test_pollen_to_cryptonote_length_less_than_11(self):
		# Creates string of length 10
		cryptonote_amount = str(10**9)
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 0.01)

	def test_pollen_to_cryptonote_length_equal_11(self):
		# Creates string of length 10
		cryptonote_amount = str(10**10)
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 0.1)

	def test_pollen_to_cryptonote_length_greater_than_11(self):
		# Creates string of length 10
		cryptonote_amount = str(10**11)
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 1.0)

	def test_pollen_to_cryptonote_prepended_zeros(self):
		# Creates string of length 10
		cryptonote_amount = '0'+str(10**6)
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 0.00001)

	def test_pollen_to_cryptonote_big_number(self):
		# Creates string of length 10
		cryptonote_amount = '1'+'0'*20+'1'
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 1000000000.000000000001)

	def test_pollen_to_cryptonote_small_number(self):
		# Creates string of length 10
		cryptonote_amount = '1'
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 0.000000000001)

if __name__ == '__main__':
	unittest.main()