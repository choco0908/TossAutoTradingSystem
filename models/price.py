from __future__ import annotations

from decimal import Decimal

from .base import BaseModel


class PriceItem(BaseModel):
    """
    현재가 정보
    """

    @property
    def symbol(self) -> str:
        return self.data["symbol"]

    @property
    def timestamp(self) -> str:
        return self.data["timestamp"]

    @property
    def last_price(self) -> Decimal:
        return Decimal(self.data["lastPrice"])

    @property
    def currency(self) -> str:
        return self.data["currency"]

    def __repr__(self):
        return (
            f"<PriceItem("
            f"symbol={self.symbol!r}, "
            f"last_price={self.last_price}, "
            f"currency={self.currency!r})>"
        )

    def __str__(self):
        return f"{self.symbol}: {self.last_price} {self.currency}"


class PriceResult(BaseModel):
    """
    현재가 조회 결과
    """

    @property
    def prices(self) -> list[PriceItem]:
        return [
            PriceItem(item)
            for item in self.data
        ]

    def get(self, symbol: str) -> PriceItem | None:
        for item in self.prices:
            if item.symbol == symbol:
                return item
        return None

    def __iter__(self):
        return iter(self.prices)

    def __len__(self):
        return len(self.prices)

    def __getitem__(self, index: int) -> PriceItem:
        return self.prices[index]

    def __repr__(self):
        return (
            f"<PriceResult("
            f"count={len(self)})>"
        )

    def __str__(self):
        return f"{len(self)} price(s)"