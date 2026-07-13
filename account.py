"""
tossinvest.account

Account API
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from base import BaseAPI
from endpoints import Endpoint


class AccountAPI(BaseAPI):
    """
    Account API

    Example
    -------

    >>> client = TossClient()

    >>> portfolio = client.account.portfolio()

    >>> portfolio["accounts"]

    >>> portfolio["summary"]

    >>> portfolio["holdings"]
    # ------------------------------------------------------------
    # 계좌 조회
    # ------------------------------------------------------------
    print_accounts(portfolio["accounts"])

    # ------------------------------------------------------------
    # 국내 주식만 조회
    # ------------------------------------------------------------

    print_holdings(portfolio["holdings"], "KR")

    # ------------------------------------------------------------
    # 미국 주식만 조회
    # ------------------------------------------------------------

    print_holdings(portfolio["holdings"], "US")
    """

    # ------------------------------------------------------------------
    # Account
    # ------------------------------------------------------------------

    def list(self) -> Dict[str, Any]:
        """
        계좌 목록 조회

        Returns
        -------
        dict
        """

        return self.get(
            Endpoint.ACCOUNTS,
        )

    # ------------------------------------------------------------------
    # Holdings
    # ------------------------------------------------------------------

    def holdings(
        self,
        *,
        symbol: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        보유 자산 조회

        Parameters
        ----------
        symbol : str, optional
            종목코드

        Returns
        -------
        dict
        """

        params: Dict[str, Any] = {}

        if symbol is not None:
            params["symbol"] = symbol

        return self.get(
            Endpoint.HOLDINGS,
            params=params if params else None,
            require_account=True,
        )

    # ------------------------------------------------------------------
    # Portfolio
    # ------------------------------------------------------------------

    def portfolio(self) -> Dict[str, Any]:
        """
        계좌 정보와 보유 종목을 함께 조회합니다.

        Returns
        -------
        dict
        {
            "accounts": {...},
            "summary": {...},
            "holdings": [...]
        }
        """

        accounts = self.list()
        holdings = self.holdings()

        account_list = accounts.get("result", [])

        holding_result = holdings.get("result", {})

        return {
            "accounts": account_list,
            "summary": {
                "totalPurchaseAmount": holding_result.get(
                    "totalPurchaseAmount", {}
                ),
                "marketValue": holding_result.get(
                    "marketValue", {}
                ),
                "profitLoss": holding_result.get(
                    "profitLoss", {}
                ),
                "dailyProfitLoss": holding_result.get(
                    "dailyProfitLoss", {}
                ),
            },
            "holdings": holding_result.get(
                "items",
                [],
            ),
        }

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def holding(
        self,
        symbol: str,
    ) -> Dict[str, Any]:
        """
        특정 종목 보유 조회
        """

        return self.holdings(
            symbol=symbol,
        )

    # ------------------------------------------------------------------
    # Account Sequence
    # ------------------------------------------------------------------

    @property
    def account_seq(self) -> str:
        """
        accountSeq 반환

        최초 호출 시 자동으로 계좌 조회 후 캐시합니다.
        """

        return self.require_account()

    # ------------------------------------------------------------------
    # Refresh
    # ------------------------------------------------------------------

    def refresh(self) -> Dict[str, Any]:
        """
        accountSeq 캐시를 초기화하고 다시 조회합니다.
        """

        self.client.account_seq = None

        if hasattr(self.client, "token_manager"):
            self.client.token_manager.account_seq = None
            self.client.token_manager.save()

        self.require_account()

        return self.list()

    # ------------------------------------------------------------------
    # Raw API
    # ------------------------------------------------------------------

    def raw_accounts(self, **params) -> Dict[str, Any]:
        """
        계좌 조회 Raw API
        """

        return self.get(
            Endpoint.ACCOUNTS,
            params=params or None,
        )

    def raw_holdings(self, **params) -> Dict[str, Any]:
        """
        보유 자산 조회 Raw API
        """

        return self.get(
            Endpoint.HOLDINGS,
            params=params or None,
            require_account=True,
        )