"""
tossinvest.order

Order API
"""

from __future__ import annotations

import time
from decimal import Decimal
from typing import Any, Dict, Optional

from base import BaseAPI
from models.order import OrderResult
from endpoints import Endpoint

Number = int | float | Decimal | str


class OrderAPI(BaseAPI):
    """
    Toss Order API
    """

    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_us_symbol(symbol: str) -> bool:
        """
        미국 종목 여부를 반환합니다.

        Parameters
        ----------
        symbol : str

        Returns
        -------
        bool
        """

        return symbol[:1].isalpha()

    @staticmethod
    def _to_string(value: Optional[Number]) -> Optional[str]:
        """
        숫자를 API 요청용 문자열로 변환합니다.

        Parameters
        ----------
        value : Number | None

        Returns
        -------
        str | None
        """

        if value is None:
            return None

        return str(value)

    def _validate_order(
            self,
            *,
            symbol: str,
            order_type: str,
            quantity: Optional[Number] = None,
            order_amount: Optional[Number] = None,
            price: Optional[Number] = None,
    ) -> None:
        """
        주문 요청의 유효성을 검사합니다.
        """

        if not symbol:
            raise ValueError("symbol is required.")

        if quantity is None and order_amount is None:
            raise ValueError(
                "Either quantity or order_amount must be provided."
            )

        if quantity is not None:
            if Decimal(str(quantity)) <= 0:
                raise ValueError(
                    "quantity must be greater than zero."
                )

        if order_amount is not None:

            if Decimal(str(order_amount)) <= 0:
                raise ValueError(
                    "order_amount must be greater than zero."
                )

            if not self._is_us_symbol(symbol):
                raise ValueError(
                    "Amount order is supported only for US stocks."
                )

            if order_type != "MARKET":
                raise ValueError(
                    "Amount order supports MARKET orders only."
                )

        if order_type == "LIMIT":

            if price is None:
                raise ValueError(
                    "price is required for LIMIT order."
                )

            if Decimal(str(price)) <= 0:
                raise ValueError(
                    "price must be greater than zero."
                )

    def _build_order_body(
            self,
            *,
            symbol: str,
            side: str,
            order_type: str,
            quantity: Optional[Number] = None,
            order_amount: Optional[Number] = None,
            price: Optional[Number] = None,
            time_in_force: Optional[str] = None,
            client_order_id: Optional[str] = None,
            confirm_high_value_order: bool = False,
    ) -> dict[str, Any]:
        """
        주문 Request Body 생성
        """

        self._validate_order(
            symbol=symbol,
            order_type=order_type,
            quantity=quantity,
            order_amount=order_amount,
            price=price,
        )

        body = {
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "clientOrderId": (
                    client_order_id
                    or self.client.order_id.next()
            ),
        }

        if quantity is not None:
            body["quantity"] = self._to_string(quantity)

        if order_amount is not None:
            body["orderAmount"] = self._to_string(order_amount)

        if price is not None:
            body["price"] = self._to_string(price)

        if time_in_force is not None:
            body["timeInForce"] = time_in_force

        if confirm_high_value_order:
            body["confirmHighValueOrder"] = True

        return body

    def _build_modify_body(
            self,
            *,
            quantity: Optional[Number] = None,
            price: Optional[Number] = None,
    ) -> dict[str, Any]:
        """
        정정 Request Body 생성
        """

        if quantity is None and price is None:
            raise ValueError(
                "Either quantity or price must be provided."
            )

        body: dict[str, Any] = {}

        if quantity is not None:

            if Decimal(str(quantity)) <= 0:
                raise ValueError(
                    "quantity must be greater than zero."
                )

            body["quantity"] = self._to_string(quantity)

        if price is not None:

            if Decimal(str(price)) <= 0:
                raise ValueError(
                    "price must be greater than zero."
                )

            body["price"] = self._to_string(price)

        return body

    # ------------------------------------------------------------------
    # Raw API
    # ------------------------------------------------------------------

    def raw_order(
            self,
            body: dict[str, Any],
    ) -> dict[str, Any]:
        """
        신규 주문 (Raw API)
        """

        return self.post(
            Endpoint.ORDERS,
            body=body,
            require_account=True,
        )

    def raw_modify(
            self,
            order_id: str,
            body: dict[str, Any],
    ) -> dict[str, Any]:
        """
        주문 정정 (Raw API)
        """

        return self.post(
            f"{Endpoint.ORDERS}/{order_id}/modify",
            body=body,
            require_account=True,
        )

    def raw_cancel(
            self,
            order_id: str,
    ) -> dict[str, Any]:
        """
        주문 취소 (Raw API)
        """

        return self.post(
            f"{Endpoint.ORDERS}/{order_id}/cancel",
            body={},
            require_account=True,
        )

    def raw_list(
            self,
            params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        주문 목록 조회 (Raw API)
        """

        return self.get(
            Endpoint.ORDERS,
            params=params,
            require_account=True,
        )

    def raw_detail(
            self,
            order_id: str,
    ) -> dict[str, Any]:
        """
        주문 상세 조회 (Raw API)
        """

        return self.get(
            f"{Endpoint.ORDERS}/{order_id}",
            require_account=True,
        )

    # ------------------------------------------------------------------
    # Internal API
    # ------------------------------------------------------------------

    def _order(
            self,
            *,
            symbol: str,
            side: str,
            order_type: str,
            quantity: Optional[Number] = None,
            order_amount: Optional[Number] = None,
            price: Optional[Number] = None,
            time_in_force: Optional[str] = None,
            client_order_id: Optional[str] = None,
            confirm_high_value_order: bool = False,
    ) -> OrderResult:
        """
        공통 주문 처리
        """

        body = self._build_order_body(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            order_amount=order_amount,
            price=price,
            time_in_force=time_in_force,
            client_order_id=client_order_id,
            confirm_high_value_order=confirm_high_value_order,
        )

        response = self.raw_order(body)
        order_id = response["result"]["orderId"]
        return self.detail(order_id)

    def wait_until_filled(
            self,
            order_id: str,
            *,
            timeout: float = 30,
            interval: float = 0.5,
    ) -> OrderResult:
        """
        주문이 체결될 때까지 대기합니다.

        Parameters
        ----------
        order_id : str
            서버 주문 ID

        timeout : float
            최대 대기 시간(초)

        interval : float
            조회 주기(초)

        Returns
        -------
        OrderResult

        Raises
        ------
        TimeoutError
            timeout 내 체결되지 않은 경우
        """

        start = time.monotonic()

        while True:

            order = self.detail(order_id)

            if order.status == "FILLED":
                return order

            if order.status in ("CANCELED", "REJECTED"):
                return order

            if time.monotonic() - start >= timeout:
                raise TimeoutError(
                    f"Order {order_id} was not filled within {timeout} seconds."
                )

            time.sleep(interval)

    # ------------------------------------------------------------------
    # Buy Orders
    # ------------------------------------------------------------------

    def buy_limit(
        self,
        symbol: str,
        quantity: Number,
        price: Number,
        *,
        time_in_force: str = "DAY",
        client_order_id: Optional[str] = None,
        confirm_high_value_order: bool = False,
    ) -> OrderResult:
        """
        지정가 매수
        """

        return self._order(
            symbol=symbol,
            side="BUY",
            order_type="LIMIT",
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
            client_order_id=client_order_id,
            confirm_high_value_order=confirm_high_value_order,
        )

    def buy_market(
        self,
        symbol: str,
        quantity: Number,
        *,
        time_in_force: str = "DAY",
        client_order_id: Optional[str] = None,
        confirm_high_value_order: bool = False,
    ) -> OrderResult:
        """
        시장가 매수
        """

        return self._order(
            symbol=symbol,
            side="BUY",
            order_type="MARKET",
            quantity=quantity,
            time_in_force=time_in_force,
            client_order_id=client_order_id,
            confirm_high_value_order=confirm_high_value_order,
        )

    def buy_amount(
        self,
        symbol: str,
        amount: Number,
        *,
        client_order_id: Optional[str] = None,
        confirm_high_value_order: bool = False,
    ) -> OrderResult:
        """
        미국주식 금액 매수
        """

        return self._order(
            symbol=symbol,
            side="BUY",
            order_type="MARKET",
            order_amount=amount,
            client_order_id=client_order_id,
            confirm_high_value_order=confirm_high_value_order,
        )

    # ------------------------------------------------------------------
    # Sell Orders
    # ------------------------------------------------------------------

    def sell_limit(
        self,
        symbol: str,
        quantity: Number,
        price: Number,
        *,
        time_in_force: str = "DAY",
        client_order_id: Optional[str] = None,
        confirm_high_value_order: bool = False,
    ) -> OrderResult:
        """
        지정가 매도
        """

        return self._order(
            symbol=symbol,
            side="SELL",
            order_type="LIMIT",
            quantity=quantity,
            price=price,
            time_in_force=time_in_force,
            client_order_id=client_order_id,
            confirm_high_value_order=confirm_high_value_order,
        )

    def sell_market(
        self,
        symbol: str,
        quantity: Number,
        *,
        time_in_force: str = "DAY",
        client_order_id: Optional[str] = None,
        confirm_high_value_order: bool = False,
    ) -> OrderResult:
        """
        시장가 매도
        """

        return self._order(
            symbol=symbol,
            side="SELL",
            order_type="MARKET",
            quantity=quantity,
            time_in_force=time_in_force,
            client_order_id=client_order_id,
            confirm_high_value_order=confirm_high_value_order,
        )

    # ------------------------------------------------------------------
    # Order Query
    # ------------------------------------------------------------------

    def list(
        self,
        *,
        status: Optional[str] = None,
        symbol: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> list[OrderResult]:
        """
        주문 목록 조회
        """

        params: dict[str, Any] = {}

        if status is not None:
            params["status"] = status

        if symbol is not None:
            params["symbol"] = symbol

        if limit is not None:
            params["limit"] = limit

        if cursor is not None:
            params["cursor"] = cursor

        response = self.raw_list(params)

        orders = response["result"]["orders"]

        return [
            OrderResult(
                client=self.client,
                data=item,
            )
            for item in orders
        ]

    def detail(
        self,
        order_id: str,
    ) -> OrderResult:
        """
        주문 상세 조회
        """

        if not order_id:
            raise ValueError("order_id is required.")

        response = self.raw_detail(order_id)

        return OrderResult(
            client=self.client,
            data=response["result"],
        )

    def open_orders(
        self,
        *,
        symbol: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> list[OrderResult]:
        """
        미체결 주문 조회
        """

        return self.list(
            status="OPEN",
            symbol=symbol,
            limit=limit,
            cursor=cursor,
        )

    def closed_orders(
        self,
        *,
        symbol: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> list[OrderResult]:
        """
        완료 주문 조회
        """

        return self.list(
            status="CLOSED",
            symbol=symbol,
            limit=limit,
            cursor=cursor,
        )

    # ------------------------------------------------------------------
    # Modify / Cancel
    # ------------------------------------------------------------------

    def modify(
        self,
        order_id: str,
        *,
        quantity: Optional[Number] = None,
        price: Optional[Number] = None,
    ) -> OrderResult:
        """
        주문 정정
        """

        if not order_id:
            raise ValueError("order_id is required.")

        body = self._build_modify_body(
            quantity=quantity,
            price=price,
        )

        response = self.raw_modify(order_id, body)

        return self.detail(
            response["result"]["orderId"]
        )

    def cancel(
        self,
        order_id: str,
    ) -> OrderResult:
        """
        주문 취소
        """

        if not order_id:
            raise ValueError("order_id is required.")

        response = self.raw_cancel(order_id)

        return self.detail(
            response["result"]["orderId"]
        )