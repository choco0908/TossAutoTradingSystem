# TossAutoTradingSystem
토스 Open API를 활용한 자동 매매 프로그램 가이드


project/  
├── credentials  
├── client.py  
└── account_example.py         # 예제


## 사용 예제
```py

from client import TossClient
from utils.printer import pprint, print_accounts, print_holdings, print_summary

def main():
    client = TossClient()
    portfolio = client.account.portfolio()

    # ------------------------------------------------------------
    # 계좌 조회
    # ------------------------------------------------------------

    print_accounts(portfolio["accounts"])

    print_summary(portfolio["summary"])

    # ------------------------------------------------------------
    # 국내 주식만 조회
    # ------------------------------------------------------------

    print_holdings(portfolio["holdings"], "KR")

    # ------------------------------------------------------------
    # 미국 주식만 조회
    # ------------------------------------------------------------

    print_holdings(portfolio["holdings"], "US")

    # ------------------------------------------------------------
    # 미국 주식 CONY 시장가 10개 매도 주문
    # ------------------------------------------------------------

    order = client.order.sell_market(
        symbol="CONY",
        quantity=10,
    )
    print(order)

    # ------------------------------------------------------------
    # 체결 시 까지 30초 대기
    # ------------------------------------------------------------

    filled = order.wait()
    print(filled)


if __name__ == "__main__":
    main()
```
