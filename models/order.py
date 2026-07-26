from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from .base import BaseModel


@dataclass(slots=True)
class OrderResult(BaseModel):
    """
    Order Result

    Parameters
    ----------
    client :
        TossClient

    data :
        Original API response
    """

    client: Any = field(repr=False)
    data: dict = field(repr=False)

    @property
    def order_id(self) -> str:
        return self.data["orderId"]

    @property
    def client_order_id(self) -> str | None:
        return self.data.get("clientOrderId")

    @property
    def symbol(self) -> str:
        return self.data["symbol"]

    @property
    def side(self) -> str:
        return self.data["side"]

    @property
    def order_type(self) -> str:
        return self.data["orderType"]

    @property
    def status(self) -> str:
        return self.data["status"]

    @property
    def quantity(self):
        return self.data.get("quantity")

    @property
    def executed_quantity(self):
        return self.data.get("executedQuantity")

    @property
    def execution(self):
        return self.data.get("execution")

    @property
    def filled_quantity(self):
        if self.execution is None:
            return None
        return self.execution.get("filledQuantity")

    @property
    def price(self):
        return self.data.get("price")

    def refresh(self):
        """
        최신 주문 정보를 조회합니다.
        """

        self.data = self.client.order.detail(self.order_id).data

        return self

    def cancel(self):
        """
        주문 취소
        """

        new_order = self.client.order.cancel(self.order_id)
        self.update(new_order)
        return new_order

    def modify(
            self,
            *,
            quantity=None,
            price=None,
    ):
        """
        주문 정정
        """
        new_order = self.client.order.modify(
            self.order_id,
            self.order_type,
            quantity=quantity,
            price=price,
        )
        self.update(new_order)
        return new_order

    def wait(
            self,
            timeout=30,
            interval=0.5,
    ):
        """
        체결 대기
        초당 최대 6회 제한
        09:00 ~ 09:10 KST: 초당 최대 3회
        """

        return self.client.order.wait_until_filled(
            self.order_id,
            timeout=timeout,
            interval=interval,
        )

    def __repr__(self):
        return (
            f"<OrderResult("
            f"symbol={self.data.get('symbol')!r}, "
            f"side={self.data.get('side')!r}, "
            f"status={self.data.get('status')!r}, "
            f"orderId={self.data.get('orderId')!r}, "
            f"price={self.data.get('price')!r}, "
            f"quantity={self.data.get('quantity')!r})>"
        )


@dataclass(slots=True)
class OrderList:
    items: list[OrderResult]
    next_cursor: str | None
    has_next: bool
