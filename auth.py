"""
tossinvest.auth

OAuth2 Client Credentials Token Manager
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from config import (
    BASE_URL,
    CREDENTIAL_FILE,
    REQUEST_TIMEOUT,
    TOKEN_FILE,
    TOKEN_MARGIN,
)
from endpoints import Endpoint
from exceptions import AuthenticationException


class TokenManager:
    """
    OAuth2 Token Manager

    Responsibilities
    ----------------
    - Load client credentials
    - Load cached access token
    - Save access token
    - Check expiration
    - Request new access token
    """

    def __init__(
        self,
        session: requests.Session,
    ) -> None:

        self.session = session

        self.client_id: Optional[str] = None
        self.client_secret: Optional[str] = None

        self.access_token: Optional[str] = None
        self.expires_at: int = 0

        self.account_seq: Optional[str] = None

        self._load_credentials()
        self._load_token()

    # ------------------------------------------------------------------
    # Credentials
    # ------------------------------------------------------------------

    def _load_credentials(self) -> None:

        if not Path(CREDENTIAL_FILE).exists():
            raise FileNotFoundError(
                f"Credential file not found: {CREDENTIAL_FILE}"
            )

        values: Dict[str, str] = {}

        with open(
            CREDENTIAL_FILE,
            encoding="utf-8",
        ) as fp:

            for line in fp:

                line = line.strip()

                if not line:
                    continue

                if ":" not in line:
                    continue

                key, value = line.split(":", 1)

                values[key.strip()] = value.strip()

        self.client_id = values.get("client_id")
        self.client_secret = values.get("client_secret")

        if not self.client_id:
            raise AuthenticationException(
                "client_id not found."
            )

        if not self.client_secret:
            raise AuthenticationException(
                "client_secret not found."
            )

    # ------------------------------------------------------------------
    # Token Cache
    # ------------------------------------------------------------------

    def _load_token(self) -> None:

        if not Path(TOKEN_FILE).exists():
            return

        try:

            with open(
                TOKEN_FILE,
                encoding="utf-8",
            ) as fp:

                data = json.load(fp)

        except Exception:
            return

        self.access_token = data.get("access_token")
        self.expires_at = data.get("expires_at", 0)
        self.account_seq = data.get("account_seq")

    def save(self) -> None:

        data = {
            "access_token": self.access_token,
            "expires_at": self.expires_at,
            "account_seq": self.account_seq,
        }

        with open(
            TOKEN_FILE,
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                data,
                fp,
                indent=4,
                ensure_ascii=False,
            )

    # ------------------------------------------------------------------
    # Token State
    # ------------------------------------------------------------------

    @property
    def expired(self) -> bool:

        if self.access_token is None:
            return True

        return time.time() >= self.expires_at

    @property
    def authorization(self) -> str:

        self.ensure_token()

        return f"Bearer {self.access_token}"

    # ------------------------------------------------------------------
    # OAuth
    # ------------------------------------------------------------------

    def authenticate(self) -> str:

        response = self.session.post(
            BASE_URL + Endpoint.TOKEN,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            timeout=REQUEST_TIMEOUT,
        )

        if not response.ok:

            raise AuthenticationException(
                response.text
            )

        token: Dict[str, Any] = response.json()

        self.access_token = token["access_token"]

        expires_in = int(token["expires_in"])

        self.expires_at = (
            int(time.time())
            + expires_in
            - TOKEN_MARGIN
        )

        self.save()

        return self.access_token

    def ensure_token(self) -> str:

        if self.expired:
            return self.authenticate()

        return self.access_token

    def refresh(self) -> str:

        return self.authenticate()

    # ------------------------------------------------------------------
    # Account
    # ------------------------------------------------------------------

    def set_account(self, account_seq: str) -> None:

        self.account_seq = account_seq
        self.save()

    def clear(self) -> None:

        self.access_token = None
        self.expires_at = 0
        self.account_seq = None

        if Path(TOKEN_FILE).exists():
            Path(TOKEN_FILE).unlink()

    # ------------------------------------------------------------------

    def __repr__(self) -> str:

        return (
            f"TokenManager("
            f"expired={self.expired}, "
            f"account_seq={self.account_seq})"
        )