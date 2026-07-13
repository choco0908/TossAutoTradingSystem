"""
tossinvest.base

Base API class used by all API modules.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

class BaseAPI:
    """
    Base class for all TossInvest API classes.

    Example
    -------
    class MarketAPI(BaseAPI):
        def price(self, **params):
            return self.get(
                Endpoint.PRICES,
                params=params
            )
    """

    def __init__(self, client: Any) -> None:
        self.client = client

    # ------------------------------------------------------------------
    # HTTP Methods
    # ------------------------------------------------------------------

    def get(
        self,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        require_account: bool = False,
    ) -> Any:

        return self.client.get(
            endpoint,
            params=params,
            require_account=require_account,
        )

    def post(
        self,
        endpoint: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        require_account: bool = False,
    ) -> Any:

        return self.client.post(
            endpoint,
            body=body,
            require_account=require_account,
        )

    def put(
        self,
        endpoint: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        require_account: bool = False,
    ) -> Any:

        return self.client.put(
            endpoint,
            body=body,
            require_account=require_account,
        )

    def patch(
        self,
        endpoint: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        require_account: bool = False,
    ) -> Any:

        return self.client.patch(
            endpoint,
            body=body,
            require_account=require_account,
        )

    def delete(
        self,
        endpoint: str,
        *,
        body: Optional[Dict[str, Any]] = None,
        require_account: bool = False,
    ) -> Any:

        return self.client.delete(
            endpoint,
            body=body,
            require_account=require_account,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @property
    def account_seq(self) -> Optional[str]:
        return self.client.account_seq

    @property
    def access_token(self) -> Optional[str]:
        return self.client.access_token

    @property
    def session(self):
        return self.client.session

    @property
    def logger(self):
        return self.client.logger

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def require_account(self) -> str:
        """
        Ensure accountSeq is available.

        Returns
        -------
        str
            accountSeq
        """
        return self.client.ensure_account()

    def ping(self) -> bool:
        """
        Check authentication status.

        Returns
        -------
        bool
        """
        self.client.authenticate()
        return True

    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"account_seq={self.account_seq}>"
        )