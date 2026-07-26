from __future__ import annotations

from decimal import Decimal
from typing import Any

from .base import BaseModel


class ExchangeRateResult(BaseModel):
    """
    환율 조회 결과
    """

    @property
    def base_currency(self) -> str:
        return self.data["baseCurrency"]

    @property
    def quote_currency(self) -> str:
        return self.data["quoteCurrency"]

    @property
    def rate(self) -> Decimal:
        return Decimal(self.data["rate"])

    @property
    def mid_rate(self) -> Decimal:
        return Decimal(self.data["midRate"])

    @property
    def basis_point(self) -> Decimal:
        return Decimal(self.data["basisPoint"])

    @property
    def rate_change_type(self) -> str:
        return self.data["rateChangeType"]

    @property
    def valid_from(self) -> str:
        return self.data["validFrom"]

    @property
    def valid_until(self) -> str:
        return self.data["validUntil"]

    @property
    def currency_pair(self) -> str:
        return f"{self.base_currency}/{self.quote_currency}"

    def __repr__(self):
        return (
            f"<ExchangeRateResult("
            f"pair={self.currency_pair!r}, "
            f"rate={self.rate}, "
            f"change={self.rate_change_type!r})>"
        )

    def __str__(self):
        arrow = {
            "UP": "▲",
            "DOWN": "▼",
            "UNCHANGED": "-",
        }.get(self.rate_change_type, "")

        return (
            f"{self.currency_pair} "
            f"{self.rate} "
            f"({arrow} 기준환율 {self.mid_rate})"
        )