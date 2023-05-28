from dotenv import load_dotenv
from pprint import pprint
from binance.error import ClientError

from core.binance_api import BinanceAPIManager


response = {
    "volume": 10000.0,
    "number": 5,
    "amountDif": 50.0,
    "side": "SELL",
    "priceMin": 200.0,
    "priceMax": 300.0
}


def main():
    try:
        client: BinanceAPIManager = BinanceAPIManager(
            base_url='https://testnet.binance.vision',
            response=response
        )
        symbol = 'BNBUSDT'
        client.create_orders(symbol)
        orders = client.get_orders(symbol)
        pprint(orders)

    except ClientError as error:
        pprint(
            f'error code = {error.error_code} \n '
            f'error message = {error.error_message}')

    except Exception as error:
        pprint(f'error = {error}')


if __name__ == '__main__':
    load_dotenv('.env')
    main()
