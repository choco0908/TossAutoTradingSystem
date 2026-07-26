from __future__ import annotations

from .base import BaseModel
from .market_session import MarketSession


class USMarketDay(BaseModel):
    """
    미국 장 운영 정보 (하루)
    """

    @property
    def date(self) -> str:
        return self.data["date"]

    def _get_session(
            self,
            name: str,
    ) -> MarketSession | None:

        integrated = self.data.get("integrated")

        if integrated is None:
            return None

        session = integrated.get(name)

        if session is None:
            return None

        return MarketSession(session)

    @property
    def day_market(self) -> MarketSession | None:
        return self._get_session("dayMarket")

    @property
    def pre_market(self) -> MarketSession | None:
        return self._get_session("preMarket")

    @property
    def regular_market(self) -> MarketSession | None:
        return self._get_session("regularMarket")

    @property
    def after_market(self) -> MarketSession | None:
        return self._get_session("afterMarket")

    def __repr__(self):
        return (
            f"<USMarketDay("
            f"date={self.date!r})>"
        )

    def __str__(self):
        return self.date


class USMarketResult(BaseModel):
    """
    미국 장 운영 정보
    """

    @property
    def today(self) -> USMarketDay:
        return USMarketDay(
            self.data["today"]
        )

    @property
    def previous_business_day(self) -> USMarketDay:
        return USMarketDay(
            self.data["previousBusinessDay"]
        )

    @property
    def next_business_day(self) -> USMarketDay:
        return USMarketDay(
            self.data["nextBusinessDay"]
        )

    def __repr__(self):
        return (
            f"<USMarketResult("
            f"today={self.today.date!r})>"
        )

    def __str__(self):
        return f"US Market ({self.today.date})"