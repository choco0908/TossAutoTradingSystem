from toss_client import TossInvestClient

#Toss API 객체 생성
client = TossInvestClient()

#Acoount 조회
#첫 API 조회에서 acess_token 발급 후 사용
accounts = client.get("/api/v1/accounts")
print(accounts)
#{'result': [{'accountNo': '0000000', 'accountSeq': 2, 'accountType': 'BROKERAGE'}]}

#삼성전자 주식 기본 정보 출력
price = client.get("/api/v1/stocks?symbols=005930")
print(price)
#{'result': [{'symbol': '005930', 'name': '삼성전자', 'englishName': 'SamsungElec', 'isinCode': 'KR7005930003', 'market': 'KOSPI', 'securityType': 'STOCK', 'isCommonShare': True, 'status': 'ACTIVE', 'currency': 'KRW', 'listDate': '1975-06-11', 'delistDate': None, 'sharesOutstanding': '5846278608', 'leverageFactor': None, 'koreanMarketDetail': {'liquidationTrading': False, 'nxtSupported': True, 'krxTradingSuspended': False, 'nxtTradingSuspended': False}}]}
