from __future__ import annotations

from decimal import Decimal

from .base import BaseModel


class TradeItem(BaseModel):
    """
    체결 정보
    """

    @property
    def price(self) -> Decimal:
        return Decimal(self.data["price"])

    @property
    def volume(self) -> Decimal:
        return Decimal(self.data["volume"])

    @property
    def timestamp(self) -> str:
        return self.data["timestamp"]

    @property
    def currency(self) -> str:
        return self.data["currency"]

    @property
    def amount(self) -> Decimal:
        return self.price * self.volume

    def __repr__(self):
        return (
            f"<TradeItem("
            f"price={self.price}, "
            f"volume={self.volume}, "
            f"timestamp={self.timestamp!r})>"
        )

    def __str__(self):
        return (
            f"{self.timestamp} | "
            f"{self.price} x {self.volume}"
        )


class TradesResult(BaseModel):
    """
    체결 조회 결과
    """

    @property
    def trades(self) -> list[TradeItem]:
        return [
            TradeItem(item)
            for item in self.data
        ]

    @property
    def total_volume(self) -> Decimal:
        return sum(
            trade.volume
            for trade in self.trades
        )

    @property
    def total_amount(self) -> Decimal:
        return sum(
            trade.amount
            for trade in self.trades
        )

    @property
    def latest(self) -> TradeItem | None:
        return self.trades[0] if self.trades else None

    def __iter__(self):
        return iter(self.trades)

    def __len__(self):
        return len(self.trades)

    def __getitem__(self, index: int) -> TradeItem:
        return self.trades[index]

    def __repr__(self):
        return (
            f"<TradesResult("
            f"count={len(self)}, "
            f"total_volume={self.total_volume})>"
        )

    def __str__(self):
        return f"{len(self)} trade(s)"