from __future__ import annotations

from decimal import Decimal

from .base import BaseModel


class Candle(BaseModel):
    """
    OHLCV 캔들
    """

    @property
    def timestamp(self) -> str:
        return self.data["timestamp"]

    @property
    def open_price(self) -> Decimal:
        return Decimal(self.data["openPrice"])

    @property
    def high_price(self) -> Decimal:
        return Decimal(self.data["highPrice"])

    @property
    def low_price(self) -> Decimal:
        return Decimal(self.data["lowPrice"])

    @property
    def close_price(self) -> Decimal:
        return Decimal(self.data["closePrice"])

    @property
    def volume(self) -> Decimal:
        return Decimal(self.data["volume"])

    @property
    def currency(self) -> str:
        return self.data["currency"]

    @property
    def change(self) -> Decimal:
        """
        종가 - 시가
        """
        return self.close_price - self.open_price

    @property
    def change_percent(self) -> Decimal:
        """
        등락률(%)
        """
        if self.open_price == 0:
            return Decimal("0")

        return (
            (self.close_price - self.open_price)
            / self.open_price
            * Decimal("100")
        )

    def __repr__(self):
        return (
            f"<Candle("
            f"time={self.timestamp!r}, "
            f"close={self.close_price}, "
            f"volume={self.volume})>"
        )

    def __str__(self):
        return (
            f"{self.timestamp} | "
            f"O:{self.open_price} "
            f"H:{self.high_price} "
            f"L:{self.low_price} "
            f"C:{self.close_price}"
        )


class CandlesResult(BaseModel):
    """
    캔들 조회 결과
    """

    @property
    def candles(self) -> list[Candle]:
        return [
            Candle(item)
            for item in self.data["candles"]
        ]

    @property
    def next_before(self) -> str | None:
        return self.data.get("nextBefore")

    @property
    def latest(self) -> Candle | None:
        return self.candles[0] if self.candles else None

    def __iter__(self):
        return iter(self.candles)

    def __len__(self):
        return len(self.candles)

    def __getitem__(self, index: int) -> Candle:
        return self.candles[index]

    def __repr__(self):
        return (
            f"<CandlesResult("
            f"count={len(self)}, "
            f"next_before={self.next_before!r})>"
        )

    def __str__(self):
        return f"{len(self)} candle(s)"