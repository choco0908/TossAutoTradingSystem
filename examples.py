"""
examples/examples.py
"""
from decimal import Decimal

from client import TossClient
from exceptions import BusinessException
from stratege_manager import StrategyManager
from strategies import BuyAmountIfBelowStrategy, BuyAmountStrategy
from utils.printer import pprint, print_accounts, print_holdings, print_summary, print_exchange_rate, print_kr_market, \
    print_us_market


def main():
    client = TossClient()
    portfolio = client.account.portfolio()

    # ---------------------------------------------------------
    # 현재 USD/KRW 환율
    # ---------------------------------------------------------
    print("=" * 80)
    print("Exchange Rate")
    print("=" * 80)

    exchange_rate = client.calendar.exchange_rate()
    print_exchange_rate(exchange_rate)

    # ---------------------------------------------------------
    # 오늘 국내 증시 마켓 정보
    # ---------------------------------------------------------
    print("=" * 80)
    print("Korea Market")
    print("=" * 80)

    kr = client.calendar.kr()
    print_kr_market(kr)

    # ---------------------------------------------------------
    # 오늘 미국 증시 마켓 정보
    # ---------------------------------------------------------
    print("=" * 80)
    print("US Market")
    print("=" * 80)

    us = client.calendar.us()
    print_us_market(us)

    # ------------------------------------------------------------
    # 계좌 조회
    # ------------------------------------------------------------

    print("=== Accounts ===")
    print_accounts(portfolio["accounts"])

    print_summary(portfolio["summary"])

    # ------------------------------------------------------------
    # 국내 주식만 조회
    # ------------------------------------------------------------

    print("\n=== KR Holdings ===")
    print_holdings(portfolio["holdings"], "KR")

    # ------------------------------------------------------------
    # 미국 주식만 조회
    # ------------------------------------------------------------

    print("\n=== US Holdings ===")
    print_holdings(portfolio["holdings"], "US")
    
    #JEPQ : 60$ 1주 지정가 주문 -> 55$로 주문 수정 -> 주문 취소
    #jepq_order = client.order.buy_limit(symbol="JEPQ", price=60, quantity=1)
    #pprint(jepq_order)
    # try:
    #     result = jepq_order.modify(price=55)
    #     pprint(result)
    # except BusinessException as e:
    #     print(e)
    # cancel = jepq_order.cancel()
    # pprint(cancel)

    # 내 주문 목록
    opens = client.order.open_orders()
    pprint(opens)

    # US Market open까지 대기
    # client.calendar.wait_until_us_open()

    # US Market 금액 주문을 특정 가격 아래에서 실행 하도록 전략 설정
    # manager = StrategyManager(client)
    # target_price = client.account.average_purchase_price("SOXL")
    # if target_price is not None:
    #     price = format(Decimal(target_price), '.2f')
    #     print(f'target price = {str(price)}')
    #     manager.add(
    #         BuyAmountIfBelowStrategy(
    #             symbol="SOXL",
    #             amount=60,
    #             target_price=price,
    #         )
    #     )
    # else:
    #     manager.add(
    #         BuyAmountStrategy(
    #             symbol="SOXL",
    #             amount=60,
    #         )
    #     )
    #
    # manager.run(interval=30)


if __name__ == "__main__":
    main()