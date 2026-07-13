"""
tossinvest.exceptions

Custom exceptions for TossInvest SDK.
"""

from __future__ import annotations

from typing import Any, Optional


class TossInvestException(Exception):
    """
    Base exception for TossInvest SDK.
    """

    def __init__(
            self,
            message: str = "",
            *,
            status_code: Optional[int] = None,
            response: Any = None,
    ) -> None:
        super().__init__(message)

        self.message = message
        self.status_code = status_code
        self.response = response

    def __str__(self) -> str:
        if self.status_code is not None:
            return f"[{self.status_code}] {self.message}"

        return self.message


# ----------------------------------------------------------------------
# Authentication
# ----------------------------------------------------------------------


class AuthenticationException(TossInvestException):
    """
    OAuth authentication failed.
    """


class TokenExpiredException(AuthenticationException):
    """
    Access token expired.
    """


class InvalidCredentialException(AuthenticationException):
    """
    Invalid client_id/client_secret.
    """


# ----------------------------------------------------------------------
# Authorization
# ----------------------------------------------------------------------

class AuthorizationException(TossInvestException):
    """
    Permission denied.
    """


class AccountRequiredException(AuthorizationException):
    """
    accountSeq is required.
    """


# ----------------------------------------------------------------------
# Request
# ----------------------------------------------------------------------

class BadRequestException(TossInvestException):
    """
    HTTP 400
    """


class ValidationException(BadRequestException):
    """
    Invalid request parameters.
    """


class NotFoundException(TossInvestException):
    """
    HTTP 404
    """


class ConflictException(TossInvestException):
    """
    HTTP 409
    """


class RateLimitException(TossInvestException):
    """
    HTTP 429
    """


# ----------------------------------------------------------------------
# Server
# ----------------------------------------------------------------------

class InternalServerException(TossInvestException):
    """
    HTTP 500
    """


class ServiceUnavailableException(TossInvestException):
    """
    HTTP 503
    """


# ----------------------------------------------------------------------
# Order
# ----------------------------------------------------------------------

class OrderException(TossInvestException):
    """
    Order failed.
    """


class OrderRejectedException(OrderException):
    """
    Order rejected.
    """


class OrderCancelledException(OrderException):
    """
    Order cancelled.
    """


class InsufficientBalanceException(OrderException):
    """
    Insufficient balance.
    """


class InsufficientQuantityException(OrderException):
    """
    Insufficient holding quantity.
    """


# ----------------------------------------------------------------------
# Market
# ----------------------------------------------------------------------

class MarketException(TossInvestException):
    """
    Market API error.
    """


class SymbolNotFoundException(MarketException):
    """
    Invalid symbol.
    """


class MarketClosedException(MarketException):
    """
    Market is closed.
    """


# ----------------------------------------------------------------------
# Conditional Order
# ----------------------------------------------------------------------

class ConditionalOrderException(OrderException):
    """
    Conditional order failed.
    """


# ----------------------------------------------------------------------
# Factory
# ----------------------------------------------------------------------

def raise_for_status(
        status_code: int,
        message: str = "",
        response: Any = None,
) -> None:
    """
    Raise an appropriate exception from an HTTP status code.
    """

    mapping = {
        400: BadRequestException,
        401: AuthenticationException,
        403: AuthorizationException,
        404: NotFoundException,
        409: ConflictException,
        429: RateLimitException,
        500: InternalServerException,
        503: ServiceUnavailableException,
    }

    exc = mapping.get(status_code, TossInvestException)

    raise exc(
        message or f"HTTP {status_code}",
        status_code=status_code,
        response=response,
    )
