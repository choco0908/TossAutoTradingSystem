from __future__ import annotations

from decimal import Decimal

from .base import BaseModel


class PriceLimitResult(BaseModel):
    """
    상/하한가 조회 결과
    (국내 주식 전용)
    """

    @property
    def timestamp(self) -> str:
        return self.data["timestamp"]

    @property
    def upper_limit_price(self) -> Decimal:
        return Decimal(self.data["upperLimitPrice"])

    @property
    def lower_limit_price(self) -> Decimal:
        return Decimal(self.data["lowerLimitPrice"])

    @property
    def currency(self) -> str:
        return self.data["currency"]

    @property
    def limit_range(self) -> Decimal:
        """
        상한가 - 하한가
        """
        return self.upper_limit_price - self.lower_limit_price

    def __repr__(self):
        return (
            f"<PriceLimitResult("
            f"upper={self.upper_limit_price}, "
            f"lower={self.lower_limit_price}, "
            f"currency={self.currency!r})>"
        )

    def __str__(self):
        return (
            f"{self.lower_limit_price} ~ "
            f"{self.upper_limit_price} {self.currency}"
        )