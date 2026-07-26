from __future__ import annotations

from base import BaseAPI
from models.candles import CandlesResult
from models.orderbook import OrderBookResult
from models.price import PriceResult
from models.price_limit import PriceLimitResult
from models.trades import TradesResult


class MarketAPI(BaseAPI):
    """
    TossInvest Market API
    """

    # ------------------------------------------------------------------
    # Raw APIs
    # ------------------------------------------------------------------

    def raw_price(
            self,
            symbols: str | list[str],
    ) -> dict:
        """
        현재가 조회

        Parameters
        ----------
        symbols : str | list[str]
            "005930"
            "005930,000660"
            ["005930", "000660"]
        """

        if isinstance(symbols, (list, tuple)):
            symbols = ",".join(symbols)

        return self.client.get(
            "/api/v1/prices",
            params={
                "symbols": symbols,
            },
        )

    def raw_orderbook(
            self,
            symbol: str,
    ) -> dict:
        """
        호가 조회
        """

        return self.client.get(
            "/api/v1/orderbook",
            params={
                "symbol": symbol,
            },
        )

    def raw_trades(
            self,
            symbol: str,
            *,
            count: int = 50,
    ) -> dict:
        """
        체결 조회
        """

        return self.client.get(
            "/api/v1/trades",
            params={
                "symbol": symbol,
                "count": count,
            },
        )

    def raw_price_limit(
            self,
            symbol: str,
    ) -> dict:
        """
        상/하한가 조회 (국내 주식)
        """

        return self.client.get(
            "/api/v1/price-limits",
            params={
                "symbol": symbol,
            },
        )

    def raw_candles(
            self,
            symbol: str,
            interval: str,
            *,
            count: int = 100,
            before: str | None = None,
            adjusted: bool = True,
    ) -> dict:
        """
        캔들 조회

        interval
        --------
        1m
        1d
        """

        params = {
            "symbol": symbol,
            "interval": interval,
            "count": count,
            "adjusted": adjusted,
        }

        if before is not None:
            params["before"] = before

        return self.client.get(
            "/api/v1/candles",
            params=params,
        )

    # ------------------------------------------------------------------
    # Public APIs
    # ------------------------------------------------------------------

    def price(
            self,
            symbols: str | list[str],
    ) -> PriceResult:
        """
        현재가 조회
        """

        response = self.raw_price(symbols)

        return PriceResult(
            response["result"]
        )

    def orderbook(
            self,
            symbol: str,
    ) -> OrderBookResult:
        """
        호가 조회
        """

        response = self.raw_orderbook(symbol)

        return OrderBookResult(
            response["result"]
        )

    def trades(
            self,
            symbol: str,
            *,
            count: int = 50,
    ) -> TradesResult:
        """
        체결 조회
        """

        response = self.raw_trades(
            symbol,
            count=count,
        )

        return TradesResult(
            response["result"]
        )

    def price_limit(
            self,
            symbol: str,
    ) -> PriceLimitResult:
        """
        상/하한가 조회
        """

        response = self.raw_price_limit(symbol)

        return PriceLimitResult(
            response["result"]
        )

    def candles(
            self,
            symbol: str,
            interval: str,
            *,
            count: int = 100,
            before: str | None = None,
            adjusted: bool = True,
    ) -> CandlesResult:
        """
        캔들 조회
        """

        response = self.raw_candles(
            symbol=symbol,
            interval=interval,
            count=count,
            before=before,
            adjusted=adjusted,
        )

        return CandlesResult(
            response["result"]
        )

    def minute_candles(
            self,
            symbol: str,
            *,
            count: int = 100,
            before: str | None = None,
            adjusted: bool = True,
    ) -> CandlesResult:
        """
        1분봉 조회
        """

        return self.candles(
            symbol=symbol,
            interval="1m",
            count=count,
            before=before,
            adjusted=adjusted,
        )

    def daily_candles(
            self,
            symbol: str,
            *,
            count: int = 100,
            before: str | None = None,
            adjusted: bool = True,
    ) -> CandlesResult:
        """
        일봉 조회
        """

        return self.candles(
            symbol=symbol,
            interval="1d",
            count=count,
            before=before,
            adjusted=adjusted,
        )
