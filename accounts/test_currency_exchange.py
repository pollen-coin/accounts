import unittest
import math
from wallet import cryptonote_to_pollen, pollen_to_cryptonote


class CurrencyExchangeTestCase(unittest.TestCase):
	"""
	Tests if Pollen to Cryptonote Conversions are correct

	Note: float() operation starts to approximate after 10 digits past the 
	decimal. 
	"""
	def test_cryptonote_to_pollen_length_less_than_11(self):
		# Creates string of length 10
		cryptonote_amount = str(10**9)
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 0.01)

	def test_cryptonote_to_pollen_length_equal_11(self):
		# Creates string of length 11
		cryptonote_amount = str(10**10)
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 0.1)

	def test_cryptonote_to_pollen_length_greater_than_11(self):
		# Creates string of length 12
		cryptonote_amount = str(10**11)
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 1.0)

	def test_cryptonote_to_pollen_prepended_zeros(self):
		# Creates string with prepended zeros
		cryptonote_amount = '000'+str(10**6)
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 0.00001)

	def test_cryptonote_to_pollen_long_number(self):
		# Creates long string starting and ending with 1
		cryptonote_amount = '1'+'0'*20+'1'
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 
							10000000000.00000000001)

	def test_cryptonote_to_pollen_small_number(self):
		# Creates a small string to test rounding
		cryptonote_amount = '1'
		self.assertEqual(cryptonote_to_pollen(cryptonote_amount), 0.00000000001)

	def test_pollen_to_cryptonote_number(self):
		# Creates big number
		pollen_amount = 1
		self.assertEqual(pollen_to_cryptonote(pollen_amount), int(10**11))

	def test_pollen_to_cryptonote_float(self):
		# Creates big number
		pollen_amount = 9.9
		self.assertEqual(pollen_to_cryptonote(pollen_amount), int(9.9*10**11))

if __name__ == '__main__':
	unittest.main()
