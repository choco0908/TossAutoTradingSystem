from __future__ import annotations

import time
from typing import List


class StrategyManager:
    """
    Execute multiple trading strategies simultaneously.
    """

    def __init__(self, client):
        self.client = client
        self._strategies: List = []

    # ---------------------------------------------------------
    # Strategy Management
    # ---------------------------------------------------------

    def add(self, strategy):
        """
        Add a strategy.
        """
        self._strategies.append(strategy)

    def remove(self, strategy):
        """
        Remove a strategy.
        """
        self._strategies.remove(strategy)

    def clear(self):
        """
        Remove all strategies.
        """
        self._strategies.clear()

    @property
    def strategies(self):
        return list(self._strategies)

    # ---------------------------------------------------------
    # Main Loop
    # ---------------------------------------------------------

    def run(
            self,
            *,
            interval: float = 1.0,
    ):
        """
        Execute strategies forever.
        """

        while True:

            if not self._strategies:
                time.sleep(interval)
                continue

            symbols = sorted({
                s.symbol
                for s in self._strategies
            })

            prices = self.client.market.price(symbols)

            price_map = {
                p.symbol: p
                for p in prices
            }

            finished = []

            for strategy in self._strategies:

                price = price_map.get(strategy.symbol)

                if price is None:
                    continue

                if strategy.check(price):
                    result = strategy.execute(self.client)

                    strategy.result = result

                    finished.append(strategy)

            for strategy in finished:
                self._strategies.remove(strategy)

            time.sleep(interval)
