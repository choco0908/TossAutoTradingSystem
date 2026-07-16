"""
tossinvest.enums

Common enums for TossInvest SDK
"""

from __future__ import annotations

from enum import Enum


class StrEnum(str, Enum):
    """
    Base string enum.
    """

    def __str__(self) -> str:
        return self.value

# ----------------------------------------------------------------------
# Market
# ----------------------------------------------------------------------

class Market(StrEnum):
    KR = "KR"
    US = "US"

# ----------------------------------------------------------------------
# Exchange
# ----------------------------------------------------------------------

class Exchange(StrEnum):
    KRX = "KRX"
    NASDAQ = "NASDAQ"
    NYSE = "NYSE"
    AMEX = "AMEX"

# ----------------------------------------------------------------------
# Order Side
# ----------------------------------------------------------------------

class Side(StrEnum):
    BUY = "BUY"
    SELL = "SELL"

# ----------------------------------------------------------------------
# Order Type
# ----------------------------------------------------------------------

class OrderType(StrEnum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

# ----------------------------------------------------------------------
# Order Status
# ----------------------------------------------------------------------

class OrderStatus(StrEnum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"

# ----------------------------------------------------------------------
# Conditional Order
# ----------------------------------------------------------------------

class TriggerType(StrEnum):
    LAST_PRICE = "LAST_PRICE"
    ASK_PRICE = "ASK_PRICE"
    BID_PRICE = "BID_PRICE"

class TriggerCondition(StrEnum):
    GTE = "GTE"
    LTE = "LTE"
    GT = "GT"
    LT = "LT"
    EQ = "EQ"

# ----------------------------------------------------------------------
# Candle Interval
# ----------------------------------------------------------------------

class CandleInterval(StrEnum):
    MIN_1 = "1m"
    MIN_3 = "3m"
    MIN_5 = "5m"
    MIN_10 = "10m"
    MIN_15 = "15m"
    MIN_30 = "30m"
    MIN_60 = "60m"
    DAY = "1d"
    WEEK = "1w"
    MONTH = "1M"

# ----------------------------------------------------------------------
# Ranking
# ----------------------------------------------------------------------

class RankingType(StrEnum):
    VOLUME = "VOLUME"
    VALUE = "VALUE"
    RISE = "RISE"
    FALL = "FALL"
    MARKET_CAP = "MARKET_CAP"
    TURNOVER = "TURNOVER"

# ----------------------------------------------------------------------
# Currency
# ----------------------------------------------------------------------

class Currency(StrEnum):
    KRW = "KRW"
    USD = "USD"

# ----------------------------------------------------------------------
# Sort
# ----------------------------------------------------------------------

class SortOrder(StrEnum):
    ASC = "ASC"
    DESC = "DESC"

# ----------------------------------------------------------------------
# Time In Force
# ----------------------------------------------------------------------

class TimeInForce(StrEnum):
    DAY = "DAY"
    CLS = "CLS"

# ----------------------------------------------------------------------
# API Environment
# ----------------------------------------------------------------------

class Environment(StrEnum):
    PRODUCTION = "production"
    SANDBOX = "sandbox"