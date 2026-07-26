from __future__ import annotations

from decimal import Decimal

from .base import BaseModel


class OrderBookItem(BaseModel):
    """
    호가 정보
    """

    @property
    def price(self) -> Decimal:
        return Decimal(self.data["price"])

    @property
    def volume(self) -> Decimal:
        return Decimal(self.data["volume"])

    def __repr__(self):
        return (
            f"<OrderBookItem("
            f"price={self.price}, "
            f"volume={self.volume})>"
        )

    def __str__(self):
        return f"{self.price} ({self.volume})"


class OrderBookResult(BaseModel):
    """
    호가 조회 결과
    """

    @property
    def timestamp(self) -> str:
        return self.data["timestamp"]

    @property
    def currency(self) -> str:
        return self.data["currency"]

    @property
    def asks(self) -> list[OrderBookItem]:
        return [
            OrderBookItem(item)
            for item in self.data["asks"]
        ]

    @property
    def bids(self) -> list[OrderBookItem]:
        return [
            OrderBookItem(item)
            for item in self.data["bids"]
        ]

    @property
    def best_ask(self) -> OrderBookItem | None:
        asks = self.asks
        return asks[0] if asks else None

    @property
    def best_bid(self) -> OrderBookItem | None:
        bids = self.bids
        return bids[0] if bids else None

    @property
    def spread(self) -> Decimal | None:
        if self.best_ask is None or self.best_bid is None:
            return None

        return self.best_ask.price - self.best_bid.price

    def __repr__(self):
        return (
            f"<OrderBookResult("
            f"asks={len(self.asks)}, "
            f"bids={len(self.bids)}, "
            f"spread={self.spread})>"
        )

    def __str__(self):
        if self.best_ask and self.best_bid:
            return (
                f"Ask {self.best_ask.price} / "
                f"Bid {self.best_bid.price}"
            )

        return "Empty OrderBook"