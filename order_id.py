from __future__ import annotations

import itertools
import uuid
from datetime import datetime


class OrderIdGenerator:
    """
    Client Order ID Generator

    Examples
    --------

    >>> gen = OrderIdGenerator()
    >>> gen.next()

    >>> gen = OrderIdGenerator(prefix="QQQ")
    >>> gen.next()
    """

    def __init__(
        self,
        prefix: str | None = None,
        separator: str = "-",
    ):
        self.prefix = prefix
        self.separator = separator
        self._sequence = itertools.count(1)

    def next(self) -> str:
        """
        Generate next client order id.

        Returns
        -------
        str
        """

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        sequence = next(self._sequence)

        parts = []

        if self.prefix:
            parts.append(self.prefix)

        parts.append(timestamp)
        parts.append(f"{sequence:06d}")

        return self.separator.join(parts)

    @staticmethod
    def uuid() -> str:
        """
        UUID based order id.
        """

        return uuid.uuid4().hex

    @staticmethod
    def timestamp() -> str:
        """
        Timestamp only.
        """

        return datetime.now().strftime("%Y%m%d%H%M%S")