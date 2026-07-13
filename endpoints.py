"""
tossinvest.endpoints

Toss Invest Open API Endpoints
"""

from __future__ import annotations


class Endpoint:
    """
    REST API Endpoint Definitions

    Endpoint paths only.
    BASE_URL is defined in config.py
    """

    ###########################################################################
    # OAuth
    ###########################################################################

    TOKEN = "/oauth2/token"

    ###########################################################################
    # Account
    ###########################################################################

    # 계좌 조회
    ACCOUNTS = "/api/v1/accounts"

    # 보유 자산 조회
    HOLDINGS = "/api/v1/holdings"

    ###########################################################################
    # Market
    ###########################################################################

    # 현재가
    PRICES = "/api/v1/prices"

    # 호가
    ORDERBOOK = "/api/v1/orderbook"

    # 체결
    TRADES = "/api/v1/trades"

    # 상/하한가
    PRICE_LIMITS = "/api/v1/price-limits"

    # 캔들
    CANDLES = "/api/v1/candles"

    ###########################################################################
    # Stock
    ###########################################################################

    # 종목 정보
    STOCKS = "/api/v1/stocks"

    # 투자주의
    STOCK_WARNING = "/api/v1/stocks/{symbol}/warnings"

    ###########################################################################
    # Calendar
    ###########################################################################

    # 환율
    EXCHANGE_RATE = "/api/v1/exchange-rate"

    # 한국장
    MARKET_CALENDAR_KR = "/api/v1/market-calendar/KR"

    # 미국장
    MARKET_CALENDAR_US = "/api/v1/market-calendar/US"

    ###########################################################################
    # Ranking
    ###########################################################################

    RANKINGS = "/api/v1/rankings"

    ###########################################################################
    # Indicator
    ###########################################################################

    # 시장지표
    INDICATOR_PRICES = "/api/v1/market-indicators/prices"

    # 지표 캔들
    INDICATOR_CANDLES = (
        "/api/v1/market-indicators/{symbol}/candles"
    )

    # 투자자별 매매동향
    INDICATOR_INVESTOR_TRADING = (
        "/api/v1/market-indicators/{symbol}/investor-trading"
    )

    ###########################################################################
    # Order
    ###########################################################################

    # 주문 생성
    ORDERS = "/api/v1/orders"

    # 주문 목록
    ORDER_LIST = "/api/v1/orders"

    # 주문 상세
    ORDER_DETAIL = "/api/v1/orders/{orderId}"

    # 주문 정정
    ORDER_MODIFICATION = "/api/v1/orders/{orderId}/modify"

    # 주문 취소
    ORDER_CANCEL = "/api/v1/orders/{orderId}/cancel"

    # 매수가능금액
    BUYING_POWER = "/api/v1/orders/buying-power"

    # 매도가능수량
    SELLABLE_QUANTITY = "/api/v1/orders/sellable-quantity"

    # 예상수수료
    COMMISSION = "/api/v1/orders/commission"

    ###########################################################################
    # Conditional Order
    ###########################################################################

    # 조건주문 생성
    CONDITIONAL_ORDERS = "/api/v1/conditional-orders"

    # 조건주문 목록
    CONDITIONAL_ORDER_LIST = "/api/v1/conditional-orders"

    # 조건주문 상세
    CONDITIONAL_ORDER_DETAIL = (
        "/api/v1/conditional-orders/{orderId}"
    )

    # 조건주문 수정
    CONDITIONAL_ORDER_MODIFICATION = (
        "/api/v1/conditional-orders/{orderId}"
    )

    # 조건주문 취소
    CONDITIONAL_ORDER_CANCEL = (
        "/api/v1/conditional-orders/{orderId}/cancel"
    )