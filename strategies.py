from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal


class BaseStrategy(ABC):
    """
    Base class of all strategies.
    """

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.result = None
        self.finished = False

    @abstractmethod
    def check(self, price) -> bool:
        pass

    @abstractmethod
    def execute(self, client):
        pass

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f"(symbol={self.symbol})>"
        )


# ----------------------------------------------------------------------
# Buy Strategies
# ----------------------------------------------------------------------

class BuyAmountStrategy(BaseStrategy):
    """
    Market buy by amount
    """

    def __init__(
            self,
            symbol: str,
            amount,
    ):
        super().__init__(symbol)

        self.amount = Decimal(str(amount))

    def check(self, amount):
        pass

    def execute(self, client):
        self.result = client.order.buy_amount_at_open(
            symbol=self.symbol,
            amount=self.amount,
        )

        self.finished = True

        return self.result

    def __repr__(self):
        return (
            f"<BuyAmountStrategy("
            f"symbol={self.symbol!r}, "
            f"amount={self.amount})>"
        )


class BuyAmountIfBelowStrategy(BaseStrategy):
    """
    Market buy by amount when price <= target_price
    """

    def __init__(
            self,
            symbol: str,
            amount,
            target_price,
    ):
        super().__init__(symbol)

        self.amount = Decimal(str(amount))
        self.target_price = Decimal(str(target_price))

    def check(self, price):
        return (
                price.last_price
                <= self.target_price
        )

    def execute(self, client):
        self.result = client.order.buy_amount_at_open(
            symbol=self.symbol,
            amount=self.amount,
        )

        self.finished = True

        return self.result

    def __repr__(self):
        return (
            f"<BuyAmountIfBelowStrategy("
            f"symbol={self.symbol!r}, "
            f"amount={self.amount}, "
            f"target={self.target_price})>"
        )


class BuyQuantityStrategy(BaseStrategy):
    """
    Market buy by quantity when price <= target_price
    """

    def __init__(
            self,
            symbol: str,
            quantity,
    ):
        super().__init__(symbol)

        self.quantity = Decimal(str(quantity))

    def check(self, quantity):
        pass

    def execute(self, client):
        self.result = client.order.buy_quantity(
            symbol=self.symbol,
            quantity=self.quantity,
        )

        self.finished = True

        return self.result

    def __repr__(self):
        return (
            f"<BuyQuantityStrategy("
            f"symbol={self.symbol!r}, "
            f"quantity={self.quantity})>"
        )


class BuyQuantityIfBelowStrategy(BaseStrategy):
    """
    Market buy by quantity when price <= target_price
    """

    def __init__(
            self,
            symbol: str,
            quantity,
            target_price,
    ):
        super().__init__(symbol)

        self.quantity = Decimal(str(quantity))
        self.target_price = Decimal(str(target_price))

    def check(self, price):
        return (
                price.last_price
                <= self.target_price
        )

    def execute(self, client):
        self.result = client.order.buy_quantity(
            symbol=self.symbol,
            quantity=self.quantity,
        )

        self.finished = True

        return self.result

    def __repr__(self):
        return (
            f"<BuyQuantityIfBelowStrategy("
            f"symbol={self.symbol!r}, "
            f"quantity={self.quantity}, "
            f"target={self.target_price})>"
        )


# ----------------------------------------------------------------------
# Sell Strategies
# ----------------------------------------------------------------------

class SellAmountStrategy(BaseStrategy):
    """
    Market sell by amount
    """

    def __init__(
            self,
            symbol: str,
            amount,
    ):
        super().__init__(symbol)

        self.amount = Decimal(str(amount))

    def check(self, price):
        pass

    def execute(self, client):
        self.result = client.order.sell_amount(
            symbol=self.symbol,
            amount=self.amount,
        )

        self.finished = True

        return self.result

    def __repr__(self):
        return (
            f"<SellAmountIfAboveStrategy("
            f"symbol={self.symbol!r}, "
            f"amount={self.amount})>"
        )


class SellAmountIfAboveStrategy(BaseStrategy):
    """
    Market sell by amount when price >= target_price
    """

    def __init__(
            self,
            symbol: str,
            amount,
            target_price,
    ):
        super().__init__(symbol)

        self.amount = Decimal(str(amount))
        self.target_price = Decimal(str(target_price))

    def check(self, price):
        return (
                price.last_price
                >= self.target_price
        )

    def execute(self, client):
        self.result = client.order.sell_amount(
            symbol=self.symbol,
            amount=self.amount,
        )

        self.finished = True

        return self.result

    def __repr__(self):
        return (
            f"<SellAmountIfAboveStrategy("
            f"symbol={self.symbol!r}, "
            f"amount={self.amount}, "
            f"target={self.target_price})>"
        )


class SellQuantityStrategy(BaseStrategy):
    """
    Market sell by quantity
    """

    def __init__(
            self,
            symbol: str,
            quantity,
    ):
        super().__init__(symbol)

        self.quantity = Decimal(str(quantity))

    def check(self, price):
        pass

    def execute(self, client):
        self.result = client.order.sell_quantity(
            symbol=self.symbol,
            quantity=self.quantity,
        )

        self.finished = True

        return self.result

    def __repr__(self):
        return (
            f"<SellQuantityIfAboveStrategy("
            f"symbol={self.symbol!r}, "
            f"quantity={self.quantity})>"
        )


class SellQuantityIfAboveStrategy(BaseStrategy):
    """
    Market sell by quantity when price >= target_price
    """

    def __init__(
            self,
            symbol: str,
            quantity,
            target_price,
    ):
        super().__init__(symbol)

        self.quantity = Decimal(str(quantity))
        self.target_price = Decimal(str(target_price))

    def check(self, price):
        return (
                price.last_price
                >= self.target_price
        )

    def execute(self, client):
        self.result = client.order.sell_quantity(
            symbol=self.symbol,
            quantity=self.quantity,
        )

        self.finished = True

        return self.result

    def __repr__(self):
        return (
            f"<SellQuantityIfAboveStrategy("
            f"symbol={self.symbol!r}, "
            f"quantity={self.quantity}, "
            f"target={self.target_price})>"
        )
