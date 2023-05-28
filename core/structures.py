from dataclasses import dataclass


@dataclass(frozen=True)
class BinanceConfig:
    base_url: str
    api_key: str
    api_secret: str


@dataclass
class Order:
    symbol: str
    side: str
    type: str
    quantity: float
    price: float
    timeInForce: str = "GTC"


@dataclass(frozen=True)
class FrontendResponse:
    volume: float
    number: int
    amountDif: float
    side: str
    priceMin: float
    priceMax: float

