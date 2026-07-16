"""
tossinvest.client

Main SDK Client
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from account import AccountAPI
from auth import TokenManager
from config import (
    BASE_URL,
    DEFAULT_HEADERS,
    LOG_FORMAT,
    LOG_LEVEL,
    MAX_RETRY,
    REQUEST_TIMEOUT,
    RETRY_BACKOFF,
    RETRY_STATUS_CODES,
)
from endpoints import Endpoint
from exceptions import AuthenticationException
from order import OrderAPI
from order_id import OrderIdGenerator

class TossClient:
    """
    TossInvest REST Client

    Example
    -------
    >>> client = TossClient()

    >>> client = TossClient(
        order_id_generator=OrderIdGenerator(
            prefix="QQQ"
        )
    )
    """

    ######################################################################
    # Constructor
    ######################################################################

    def __init__(
        self,
        base_url: str = BASE_URL,
        order_id_generator: OrderIdGenerator | None = None,
    ) -> None:
        self.base_url = base_url
        self.logger = self._create_logger()
        self.session = requests.Session()
        self._configure_session()
        self.token_manager = TokenManager(
            self.session
        )

        # API Registry

        self.account = AccountAPI(self)
        self.order_id = (
                order_id_generator
                or OrderIdGenerator()
        )
        self.order = OrderAPI(self)
        #self.market = MarketAPI(self)
        #self.stock = StockAPI(self)
        #self.calendar = CalendarAPI(self)
        #self.ranking = RankingAPI(self)
        #self.indicator = IndicatorAPI(self)

    ######################################################################
    # Logger
    ######################################################################

    def _create_logger(self) -> logging.Logger:
        logger = logging.getLogger(
            "tossinvest"
        )

        if logger.handlers:
            return logger

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            LOG_FORMAT
        )

        handler.setFormatter(
            formatter
        )

        logger.addHandler(handler)
        logger.setLevel(LOG_LEVEL)
        return logger

    ######################################################################
    # Session
    ######################################################################

    def _configure_session(self) -> None:

        retry = Retry(
            total=MAX_RETRY,
            connect=MAX_RETRY,
            read=MAX_RETRY,
            backoff_factor=RETRY_BACKOFF,
            status_forcelist=RETRY_STATUS_CODES,
            allowed_methods=[
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
            ],
        )

        adapter = HTTPAdapter(
            max_retries=retry
        )

        self.session.mount(
            "https://",
            adapter,
        )

        self.session.mount(
            "http://",
            adapter,
        )

        self.session.headers.update(
            DEFAULT_HEADERS
        )

    ######################################################################
    # Properties
    ######################################################################

    @property
    def access_token(self) -> Optional[str]:
        return self.token_manager.access_token

    @property
    def account_seq(self) -> Optional[str]:
        return self.token_manager.account_seq

    @account_seq.setter
    def account_seq(
        self,
        value: Optional[str],
    ) -> None:
        self.token_manager.account_seq = value

    ######################################################################
    # Authentication
    ######################################################################

    def authenticate(self) -> None:
        self.token_manager.ensure_token()

    ######################################################################
    # Account
    ######################################################################

    def ensure_account(self) -> str:
        """
        Automatically obtain accountSeq.

        accountSeq is cached in token.json.
        """

        if self.account_seq:
            return self.account_seq

        self.logger.info(
            "Loading account sequence..."
        )

        result = self.get(
            Endpoint.ACCOUNTS,
            require_account=False,
        )

        accounts = result

        # Response normalization

        if isinstance(accounts, dict):
            if "result" in accounts:
                accounts = accounts["result"]
            elif "results" in accounts:
                accounts = accounts["results"]
            elif "accounts" in accounts:
                accounts = accounts["accounts"]
            elif "data" in accounts:
                accounts = accounts["data"]
        if not accounts:
            raise RuntimeError(
                "No account found."
            )

        self.account_seq = accounts[0]["accountSeq"]
        self.token_manager.save()
        return self.account_seq

    ######################################################################
    # Headers
    ######################################################################

    def headers(
        self,
        *,
        require_account: bool = False,
    ) -> Dict[str, str]:
        """
        Build request headers.
        """

        self.authenticate()

        headers = dict(DEFAULT_HEADERS)

        headers["Authorization"] = (
            f"Bearer {self.access_token}"
        )

        if require_account:
            headers[
                "X-Tossinvest-Account"
            ] = str(self.ensure_account())

        return headers

    ######################################################################
    # Request Engine
    ######################################################################

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        require_account: bool = False,
        retry: bool = True,
    ) -> Any:
        """
        Generic HTTP request.
        """

        url = self.base_url + endpoint

        self.logger.info(
            "%s %s",
            method.upper(),
            endpoint,
        )

        response = self.session.request(
            method=method.upper(),
            url=url,
            headers=self.headers(
                require_account=require_account
            ),
            params=params,
            json=body,
            timeout=REQUEST_TIMEOUT,
        )

        self.logger.info(
            "HTTP %s",
            response.status_code,
        )

        # Access Token Expired

        if (
            response.status_code == 401
            and retry
        ):
            self.logger.warning(
                "Access token expired. Refreshing..."
            )

            self.token_manager.refresh()
            return self.request(
                method,
                endpoint,
                params=params,
                body=body,
                require_account=require_account,
                retry=False,
            )

        # Rate Limit

        if (
            response.status_code == 429
            and retry
        ):
            retry_after = response.headers.get(
                "Retry-After"
            )

            if retry_after:
                self.logger.warning(
                    "Rate limited. Waiting %s sec...",
                    retry_after,
                )

                time.sleep(
                    int(retry_after)
                )

                return self.request(
                    method,
                    endpoint,
                    params=params,
                    body=body,
                    require_account=require_account,
                    retry=False,
                )

        # Error

        if not response.ok:
            raise AuthenticationException(
                response.text
            )
        if (
            response.text is None
            or response.text == ""
        ):
            return None

        return response.json()

    ######################################################################
    # HTTP Shortcuts
    ######################################################################

    def get(
        self,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        require_account: bool = False,
    ) -> Any:

        return self.request(
            "GET",
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

        return self.request(
            "POST",
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

        return self.request(
            "PUT",
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

        return self.request(
            "PATCH",
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
        return self.request(
            "DELETE",
            endpoint,
            body=body,
            require_account=require_account,
        )

    ######################################################################
    # Utilities
    ######################################################################

    def ping(self) -> bool:
        """
        Verify authentication.

        Returns
        -------
        bool
        """
        self.authenticate()
        return True

    def health(self) -> dict:
        """
        SDK health information.

        Returns
        -------
        dict
        """
        return {
            "authenticated": not self.token_manager.expired,
            "account_seq": self.account_seq,
            "base_url": self.base_url,
        }

    def clear_token(self) -> None:
        """
        Remove cached token.
        """
        self.token_manager.clear()

    def refresh_token(self) -> None:
        """
        Force OAuth authentication.
        """
        self.token_manager.refresh()

    ######################################################################
    # Context Manager
    ######################################################################

    def close(self) -> None:
        """
        Close HTTP session.
        """
        self.session.close()

    def __enter__(self) -> "TossClient":
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:

        self.close()

    ######################################################################
    # Representation
    ######################################################################

    @property
    def version(self) -> str:
        """
        SDK version.
        """

        from .config import SDK_VERSION
        return SDK_VERSION

    @property
    def user_agent(self) -> str:
        """
        SDK User-Agent.
        """

        from .config import USER_AGENT
        return USER_AGENT

    def __repr__(self) -> str:

        authenticated = (
            "Yes"
            if not self.token_manager.expired
            else "No"
        )

        return (
            f"<TossClient("
            f"authenticated={authenticated}, "
            f"account_seq={self.account_seq}, "
            f"version={self.version})>"
        )

    __str__ = __repr__