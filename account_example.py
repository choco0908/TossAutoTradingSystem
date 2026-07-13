"""
examples/account_example.py
"""

from pprint import pprint
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

if __name__ == "__main__":
    main()