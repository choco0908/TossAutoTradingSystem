"""
tossinvest.exceptions

Custom exceptions for TossInvest SDK.
"""

from __future__ import annotations

from typing import Any, Optional


class TossInvestException(Exception):

    def __init__(
            self,
            *,
            request_id=None,
            code=None,
            message=None,
            data=None,
    ):
        self.request_id = request_id
        self.code = code
        self.message = message
        self.data = data or {}

        super().__init__(message)

    def __str__(self):
        return (
            f"[{self.code}] "
            f"{self.message}"
        )


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

class AccountRequiredException(TossInvestException):
    """
    accountSeq is required.
    """


# ----------------------------------------------------------------------
# Request
# ----------------------------------------------------------------------

class BadRequestException(TossInvestException):
    """
    HTTP 400
    잘못된 요청. 필수 파라미터 누락
    """


class AuthorizationException(TossInvestException):
    """
    HTTP 401
    인증 실패
    """


class PermissionException(TossInvestException):
    """
    HTTP 403
    """


class NotFoundException(TossInvestException):
    """
    HTTP 404
    """


class ConflictException(TossInvestException):
    """
    HTTP 409
    중복 요청
    """


class BusinessException(TossInvestException):
    """
    HTTP 422
    비즈니스 규칙 위반
    """


class RateLimitException(TossInvestException):
    """
    HTTP 429
    요청 한도 초과
    """


# ----------------------------------------------------------------------
# Server
# ----------------------------------------------------------------------

class InternalServerException(TossInvestException):
    """
    HTTP 500
    주문 처리 중 일시적 오류 또는 시스템 점검
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


class TimeoutException(Exception):
    """
    Raised when a timeout occurs while waiting for a condition.
    """

    def __init__(self, message: str = "Operation timed out."):
        super().__init__(message)