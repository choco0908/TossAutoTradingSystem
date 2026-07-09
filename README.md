# TossAutoTradingSystem
토스 Open API를 활용한 자동 매매 프로그램 가이드


project/  
├── credentials  
├── toss_client.py      # REST API 공통 클래스  
└── examples.py         # 예제


## 사용 예제
```py
from toss_client import TossInvestClient
client = TossInvestClient()

# 계좌 정보 조회
accounts = client.get("/v1/accounts")
print(accounts)
```
