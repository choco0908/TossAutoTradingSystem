"""
examples/account_example.py
"""

from client import TossClient
from utils.printer import pprint, print_accounts, print_holdings, print_summary

def main():
    client = TossClient()
    portfolio = client.account.portfolio()

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

    order = client.order.sell_market(
        symbol="CONY",
        quantity=10,
    )
    print(order)

    filled = order.wait()

    print(filled)

    # order = client.order.buy_amount(
    #     symbol="DFEN",
    #     amount=60,
    # )
    #
    # print(order)
    #
    # filled = order.wait()
    #
    # print(filled)


if __name__ == "__main__":
    main()