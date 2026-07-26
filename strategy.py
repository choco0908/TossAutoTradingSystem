from __future__ import annotations

import time
from decimal import Decimal

from exceptions import TimeoutException
from base import BaseAPI


class Strategy(BaseAPI):
    """
    High-level trading strategies built on top of MarketAPI and OrderAPI.

    This class never calls the OpenAPI directly.
    It only combines market.py and order.py.
    """

    # ------------------------------------------------------------------
    # Price Waiting
    # ------------------------------------------------------------------

    def wait_until_price(
        self,
        symbol: str,
        target_price: Decimal | float | int | str,
        *,
        operator: str = "<=",
        timeout: int | None = None,
        interval: float = 1.0,
    ):
        """
        Wait until a stock reaches the target price.

        Parameters
        ----------
        symbol : str

        target_price : Decimal

        operator :
            <=
            <
            >=
            >
            ==
            !=

        timeout :
            seconds

        interval :
            polling interval (seconds)

        Returns
        -------
        PriceItem
        """

        target_price = Decimal(str(target_price))

        start = time.time()

        while True:

            price = self.client.market.price(symbol).get(symbol)

            if price is None:
                raise RuntimeError(
                    f"Cannot retrieve price: {symbol}"
                )

            current = price.last_price

            matched = (
                (operator == "<=" and current <= target_price)
                or (operator == "<" and current < target_price)
                or (operator == ">=" and current >= target_price)
                or (operator == ">" and current > target_price)
                or (operator == "==" and current == target_price)
                or (operator == "!=" and current != target_price)
            )

            if matched:
                return price

            if (
                timeout is not None
                and time.time() - start >= timeout
            ):
                raise TimeoutException(
                    f"Target price not reached: "
                    f"{symbol} ({target_price})"
                )

            time.sleep(interval)

    # ------------------------------------------------------------------
    # Buy
    # ------------------------------------------------------------------

    def buy_amount_if_below(
        self,
        symbol: str,
        amount,
        target_price,
        *,
        timeout: int | None = None,
        interval: float = 1.0,
    ):
        """
        Market Buy when current price <= target price.
        """

        self.wait_until_price(
            symbol=symbol,
            target_price=target_price,
            operator="<=",
            timeout=timeout,
            interval=interval,
        )

        return self.client.order.buy_amount(
            symbol=symbol,
            amount=amount,
        )

    def buy_amount_if_above(
        self,
        symbol,
        amount,
        target_price,
        *,
        timeout=None,
        interval=1.0,
    ):
        """
        Market Buy when current price >= target price.
        """

        self.wait_until_price(
            symbol=symbol,
            target_price=target_price,
            operator=">=",
            timeout=timeout,
            interval=interval,
        )

        return self.client.order.buy_amount(
            symbol=symbol,
            amount=amount,
        )

    # ------------------------------------------------------------------
    # Sell
    # ------------------------------------------------------------------

    def sell_quantity_if_above(
        self,
        symbol,
        quantity,
        target_price,
        *,
        timeout=None,
        interval=1.0,
    ):
        """
        Market Sell when current price >= target price.
        """

        self.wait_until_price(
            symbol=symbol,
            target_price=target_price,
            operator=">=",
            timeout=timeout,
            interval=interval,
        )

        return self.client.order.sell_quantity(
            symbol=symbol,
            quantity=quantity,
        )

    def sell_quantity_if_below(
        self,
        symbol,
        quantity,
        target_price,
        *,
        timeout=None,
        interval=1.0,
    ):
        """
        Stop Loss
        """

        self.wait_until_price(
            symbol=symbol,
            target_price=target_price,
            operator="<=",
            timeout=timeout,
            interval=interval,
        )

        return self.client.order.sell_quantity(
            symbol=symbol,
            quantity=quantity,
        )

    # ------------------------------------------------------------------
    # Market Session
    # ------------------------------------------------------------------

    def wait_until_us_regular_market(
        self,
        *,
        interval: int = 30,
    ):
        """
        Wait until the US regular market opens.
        """

        while True:

            market = self.client.market.us_market()

            now = time.time()

            start = market.today.regular_market.start_time.timestamp()

            if now >= start:
                return

            time.sleep(interval)

    def wait_until_kr_regular_market(
        self,
        *,
        interval: int = 30,
    ):
        """
        Wait until the KR regular market opens.
        """

        while True:

            market = self.client.market.korea_market()

            now = time.time()

            start = market.today.regular_market.start_time.timestamp()

            if now >= start:
                return

            time.sleep(interval)