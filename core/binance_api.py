import os

from random import uniform
from dataclasses import asdict
from binance.spot import Spot

from core.structures import (
    BinanceConfig,
    FrontendResponse,
    Order,
)


class BinanceAPIManager:
    """
    A class that implements standard methods
     for working with the Binance API.
    """
    def __init__(
            self,
            response: dict,
            base_url: str | None = 'https://testnet.binance.vision'
    ):
        config: BinanceConfig = BinanceConfig(
            base_url,
            os.environ.get('API_KEY'),
            os.environ.get('API_SECRET'),
        )

        self.binance_client: Spot = Spot(**asdict(config))
        self.response = FrontendResponse(**response)

    @staticmethod
    def create_volumes(response: FrontendResponse) -> list[dict]:
        """
        Returns a list of data dictionaries in pairs (price, quantity).
        """
        data: list = list()

        for i in range(response.number):
            volume_one_order: float = response.volume / response.number
            volume_random: float = uniform(
                volume_one_order - response.amountDif,
                volume_one_order + response.amountDif
            )
            price: float = uniform(
                response.priceMin,
                response.priceMax
            )
            quantity_of_coins: float = volume_random / price

            data.append({
                'price': round(price, 2),
                'quantity': round(quantity_of_coins, 2),
            })

        return data

    def create_orders(
            self,
            symbol: str,
            type_order: str = 'LIMIT',
            timeInForce: str = 'GTC',
    ) -> None:
        """
        Creates orders based on our calculated data (price, quantity).
        """
        data: list[dict] = self.create_volumes(self.response)

        for volume in data:
            order: Order = Order(
                symbol=symbol,
                side=self.response.side,
                type=type_order,
                quantity=volume.get('quantity'),
                price=volume.get('price'),
                timeInForce=timeInForce,
            )

            self.binance_client.new_order(**asdict(order))

    def get_price_filter(self, symbol: str, filter_type: str) -> dict:
        """
        Allows you to get the conditions (filters) to create orders for a symbol.
        """
        data_from_api = self.binance_client.exchange_info(symbol)
        symbol_info = next(filter(lambda x: x['symbol'] == symbol, data_from_api['symbols']))

        return next(filter(lambda x: x['filterType'] == filter_type, symbol_info['filters']))

    def get_orders(self, symbol: str, **kwargs) -> list[dict]:
        """
        Returns the list of created orders for a specific symbol.
        """
        return self.binance_client.get_orders(symbol=symbol, **kwargs)

    def close_orders(self, symbol: str) -> None | dict:
        """
        Closes the active orders.
        Closes all ACTIVE, PARTIALLY FILLED or NEW orders.
        """
        response = None

        for order in self.get_orders(symbol):
            if order.get('status') == ('ACTIVE' or 'PARTIALLY_FILLED' or 'NEW'):
                response = self.binance_client.cancel_order(
                    symbol=symbol,
                    orderId=order.get('orderId')
                )

        return response
