import unittest
from models.black_scholes import black_scholes

class TestBlackScholes(unittest.TestCase):
    def test_call_price(self):
        price = black_scholes(100, 100, 1, 0.05, 0.2, 'call')
        self.assertAlmostEqual(price, 10.45, places=1)

    def test_put_price(self):
        price = black_scholes(100, 100, 1, 0.05, 0.2, 'put')
        self.assertAlmostEqual(price, 5.57, places=1)

if __name__ == "__main__":
    unittest.main()