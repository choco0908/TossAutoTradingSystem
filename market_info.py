"""
tossinvest.calendar

Calendar API
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

from base import BaseAPI
from endpoints import Endpoint
from exceptions import MarketClosedException
from models.exchange_rate import ExchangeRateResult
from models.korea_market import KoreaMarketResult
from models.us_market import USMarketResult


class MarketInfo(BaseAPI):
    """
    Calendar API

    Example
    -------
    >>> client.calendar.exchange_rate()

    >>> client.calendar.kr()

    >>> client.calendar.us()

    >>> client.calendar.us(date="2026-01-01")
    """

    # ------------------------------------------------------------------
    # Exchange Rate
    # ------------------------------------------------------------------

    def exchange_rate(
            self,
            *,
            date_time: str | None = None,
            base_currency: str = "USD",
            quote_currency: str = "KRW",
    ) -> ExchangeRateResult:
        """
        환율 조회
        """

        response = self.raw_exchange_rate(
            date_time=date_time,
            base_currency=base_currency,
            quote_currency=quote_currency,
        )

        return ExchangeRateResult(
            response["result"]
        )

    # ------------------------------------------------------------------
    # Korea Market Calendar
    # ------------------------------------------------------------------

    def kr(
            self,
            *,
            date: str | None = None,
    ) -> KoreaMarketResult:
        """
        국내 장 운영 정보 조회
        """

        response = self.raw_korea_market(
            date=date,
        )

        return KoreaMarketResult(
            response["result"]
        )

    # ------------------------------------------------------------------
    # US Market Calendar
    # ------------------------------------------------------------------

    def us(
            self,
            *,
            date: str | None = None,
    ) -> USMarketResult:
        """
        미국 장 운영 정보 조회
        """

        response = self.raw_us_market(
            date=date,
        )

        return USMarketResult(
            response["result"]
        )

    # ------------------------------------------------------------------
    # Generic Calendar
    # ------------------------------------------------------------------

    def market(
            self,
            market: str,
            date: Optional[str] = None,
            **kwargs,
    ) -> Dict[str, Any]:
        """
        시장 일정 조회

        Parameters
        ----------
        market : str
            KR / US
        """

        market = market.upper()

        if market == "KR":
            return self.kr(date=date, **kwargs)

        if market == "US":
            return self.us(date=date, **kwargs)

        raise ValueError(f"Unsupported market: {market}")

    # ------------------------------------------------------------------
    # US Market Hours
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_market_time(value: Optional[str]) -> Optional[datetime]:
        """
        market-calendar 응답의 시간 문자열을 datetime으로 변환합니다.
        NOTE: 실제 응답의 timezone 표기를 확인 후 필요하면 파싱 로직을
        조정해야 합니다. offset이 없는 문자열은 UTC로 간주합니다.
        """

        if value is None:
            return None

        parsed = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed

    def next_us_session(
            self,
            *,
            session: str = "regularMarket",
    ) -> Tuple[Optional[datetime], datetime]:
        """
        지정한 미국 장 세션의 (개장 시각, 폐장 시각)을 조회합니다.
        오늘 해당 세션이 이미 진행 중이면 개장 시각은 None으로 반환됩니다.
        오늘 세션이 이미 끝났거나 휴장이면 다음 영업일(nextBusinessDay) 기준으로 조회합니다.

        Parameters
        ----------
        session : str
            "dayMarket" / "preMarket" / "regularMarket" / "afterMarket"
            중 하나. 기본값은 정규장(regularMarket).

        Returns
        -------
        tuple[datetime | None, datetime]
            (개장 시각 또는 None, 폐장 시각)
        """

        response = self.raw_us_market()
        result = response["result"]
        now = datetime.now(timezone.utc)

        for day_key in ("today", "nextBusinessDay"):
            market_day = result.get(day_key)
            if not market_day:
                continue
            session_info = market_day.get(session)
            if not session_info:
                continue
            open_at = self._parse_market_time(
                session_info.get("startTime")
            )
            close_at = self._parse_market_time(
                session_info.get("endTime")
            )
            if close_at is None or now >= close_at:
                continue
            already_open = open_at is not None and now >= open_at
            return (None if already_open else open_at), close_at

        raise MarketClosedException(
            message=(
                f"'{session}' 세션 정보를 today/nextBusinessDay에서 "
                f"찾을 수 없습니다."
            ),
        )

    def is_us_market_open(
            self,
            *,
            session: str = "regularMarket",
    ) -> bool:
        """
        지정한 미국 장 세션이 현재 열려 있는지 확인합니다.
        """
        open_at, _ = self.next_us_session(session=session)
        return open_at is None

    def wait_until_us_open(
        self,
        *,
        session: str = "regularMarket",
        poll_interval: float = 30,
        refresh_interval: float = 1800,
        timeout: Optional[float] = None,
    ) -> None:
        """
        지정한 미국 장 세션이 열릴 때까지 대기합니다.

        Parameters
        ----------
        session : str
            대기할 세션. 기본값은 정규장(regularMarket).

        poll_interval : float
            대기 상태를 로그로 남기는 주기(초). 이 값으로는 API를 다시
            조회하지 않고, 로컬에서 남은 시간을 계산합니다.

        refresh_interval : float
            장 운영 정보를 실제로 다시 조회(재검증)하는 주기(초). 대기가
            길어질 경우 스케줄 변경(임시 휴장 등)을 반영하기 위해
            주기적으로 재조회합니다. 기본값 1800초(30분).

        timeout : float, optional
            최대 대기 시간(초). None이면 장이 열릴 때까지 무기한 대기합니다.

        Raises
        ------
        TimeoutError
            timeout 내에 장이 열리지 않은 경우
        MarketClosedException
            장 운영 정보를 확인할 수 없는 경우
        """

        start = time.monotonic()

        open_at, close_at = self.next_us_session(session=session)
        last_refresh = time.monotonic()

        while True:

            if open_at is None:
                self.logger.info(
                    "US market session '%s' is open (closes at %s).",
                    session,
                    close_at,
                )
                return

            elapsed = time.monotonic() - start

            if timeout is not None and elapsed >= timeout:
                raise TimeoutError(
                    f"US market session '{session}' did not open "
                    f"within {timeout} seconds."
                )

            remaining = (
                open_at - datetime.now(timezone.utc)
            ).total_seconds()

            if remaining <= 0:
                # 시각상으로는 열렸어야 하므로 최신 상태를 다시 확인합니다.
                open_at, close_at = self.next_us_session(session=session)
                last_refresh = time.monotonic()
                continue

            hours, rem = divmod(int(remaining), 3600)
            minutes, seconds = divmod(rem, 60)

            sleep_for = max(min(remaining, poll_interval), 1)

            if timeout is not None:
                sleep_for = min(sleep_for, timeout - elapsed)

            self.logger.info(
                "US market session '%s' opens in %02d:%02d:%02d "
                "(at %s). Sleeping %.0f sec...",
                session,
                hours,
                minutes,
                seconds,
                open_at,
                sleep_for,
            )

            time.sleep(max(sleep_for, 0))

            if time.monotonic() - last_refresh >= refresh_interval:
                open_at, close_at = self.next_us_session(session=session)
                last_refresh = time.monotonic()

    # ------------------------------------------------------------------
    # Raw APIs
    # ------------------------------------------------------------------

    def raw_exchange_rate(
            self,
            *,
            date_time: str | None = None,
            base_currency: str = "USD",
            quote_currency: str = "KRW",
    ) -> dict:
        """
        환율 조회
        """

        params = {
            "baseCurrency": base_currency,
            "quoteCurrency": quote_currency,
        }

        if date_time is not None:
            params["dateTime"] = date_time

        return self.client.get(
            Endpoint.EXCHANGE_RATE,
            params=params,
        )

    def raw_korea_market(
            self,
            *,
            date: str | None = None,
    ) -> dict:
        """
        국내 장 운영 정보 조회
        """

        params = {}

        if date is not None:
            params["date"] = date

        return self.client.get(
            Endpoint.MARKET_CALENDAR_KR,
            params=params,
        )

    def raw_us_market(
            self,
            *,
            date: str | None = None,
    ) -> dict:
        """
        미국 장 운영 정보 조회
        """

        params = {}

        if date is not None:
            params["date"] = date

        return self.client.get(
            Endpoint.MARKET_CALENDAR_US,
            params=params,
        )
