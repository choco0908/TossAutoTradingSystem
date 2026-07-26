from __future__ import annotations

from typing import Optional

from .base import BaseModel


class MarketSession(BaseModel):
    """
    장 세션 정보
    """

    @property
    def start_time(self) -> str:
        return self.data["startTime"]

    @property
    def end_time(self) -> str:
        return self.data["endTime"]

    @property
    def single_price_auction_start_time(self) -> Optional[str]:
        return self.data.get("singlePriceAuctionStartTime")

    @property
    def single_price_auction_end_time(self) -> Optional[str]:
        return self.data.get("singlePriceAuctionEndTime")

    def to_dict(self) -> dict:
        return dict(self.data)

    def __repr__(self):
        return (
            f"<MarketSession("
            f"start_time={self.start_time!r}, "
            f"end_time={self.end_time!r})>"
        )

    def __str__(self):
        return f"{self.start_time} ~ {self.end_time}"