import unittest

from dotenv import load_dotenv
from binance.error import ClientError

from core.binance_api import BinanceAPIManager


load_dotenv('.env')


class BinanceApiManagerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        response1 = {
            "volume": 10000.0,
            "number": 5,
            "amountDif": 50.0,
            "side": "SELL",
            "priceMin": 200.0,
            "priceMax": 300.0
        }
        self.binanceApi1 = BinanceAPIManager(response=response1)
        self.result1 = self.binanceApi1.create_volumes(
            response=self.binanceApi1.response
        )
        self.symbol1 = 'BTCUSDT'

        response2 = {
            "volume": 123.0,
            "number": 0,
            "amountDif": 50.0,
            "side": "BUY",
            "priceMin": 1.0,
            "priceMax": 9999.0
        }
        self.binanceApi2 = BinanceAPIManager(response=response2)
        self.result2 = self.binanceApi2.create_volumes(
            response=self.binanceApi2.response
        )
        self.symbol2 = 'BNBUSDT'

    def test_create_volumes(self) -> None:
        self.assertIsInstance(self.result1, list)
        self.assertIsInstance(self.result2, list)
        self.assertEqual(self.result2, list())

        for data in self.result1:
            self.assertIsInstance(data, dict)
            self.assertIn('price', data)
            self.assertIn('quantity', data)
            self.assertGreaterEqual(data.get('price'), 0)
            self.assertGreaterEqual(data.get('quantity'), 0)

    def test_create_orders(self) -> None:
        order1 = self.binanceApi1
        order2 = self.binanceApi1

        with self.assertRaises(ClientError):
            order1.create_orders(self.symbol1)
            order2.create_orders(self.symbol1)

        try:
            # Should not cause an error or
            # the price is out of range
            order1.create_orders(self.symbol2)
            order2.create_orders(self.symbol2)

        except ClientError:
            self.fail()

    def test_get_price_filter(self) -> None:
        response1 = self.binanceApi1.get_price_filter(self.symbol1, 'PERCENT_PRICE_BY_SIDE')
        response2 = self.binanceApi2.get_price_filter(self.symbol2, 'PRICE_FILTER')

        self.assertIsInstance(response1, dict)
        self.assertIsInstance(response2, dict)
        self.assertIn('minPrice', response2)
        self.assertIn('bidMultiplierUp', response1)

    def test_get_orders(self) -> None:
        response1 = self.binanceApi1.get_orders(self.symbol1)
        response2 = self.binanceApi2.get_orders(self.symbol2)
        print(response1, '\n\n')
        print(response2)

        self.assertIsInstance(response1, list)
        self.assertIsInstance(response2, list)

        for order1 in response1:
            self.assertIsInstance(order1, dict)
            self.assertIn('symbol', order1)
            self.assertEqual(order1.get('symbol'), self.symbol1)
            self.assertIn('price', order1)

        for order2 in response2:
            self.assertIsInstance(order2, dict)
            self.assertIn('symbol', order2)
            self.assertEqual(order2.get('symbol'), self.symbol2)
            self.assertIn('price', order2)

    def test_close_open_orders(self) -> None:
        result1 = self.binanceApi1.close_orders(self.symbol1)
        result2 = self.binanceApi2.close_orders(self.symbol2)

        self.assertEqual(result1, None)
        self.assertEqual(result2, None)


if __name__ == '__main__':
    unittest.main()
