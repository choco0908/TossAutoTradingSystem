# TossAutoTradingSystem
토스 Open API를 활용한 자동 매매 프로그램 가이드


project/  
├── credentials  
├── client.py  
└── account_example.py         # 예제


## 사용 예제
```py
from client import TossClient
from utils.printer import pprint
client = TossClient()

portfolio = client.account.portfolio()

pprint(portfolio["accounts"])

pprint(portfolio["summary"])

pprint(portfolio["holdings"])
```
