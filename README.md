# 📈 TossAutoTradingSystem

> **토스증권 Open API 기반 파이썬 자동매매 SDK 및 트레이딩 프레임워크**
> 
> 토스증권 API를 쉽고 안전하게 활용하여 계좌 관리, 시세 데이터 조회(Candles, Orderbook, Trades), 전략(Strategy) 엔진 운영, 주문 자동화(매수/매도)를 구현할 수 있는 Python 클라이언트 라이브러리입니다.

---

## 📸 주요 특징 (Key Features)

- **통합 API 클라이언트 (`client.py`)**: 계좌(`account`), 시세(`market`), 주문(`order`) 기능 단일 제공
- **시세 정보 지원 (`market.py`, `models/`)**: 호가(Orderbook), 체결 내역(Trades), 캔들 데이터(Candles), 환율 및 시장 세션 조회
- **전략 엔진 트레이딩 (`strategy.py`, `stratege_manager.py`)**: 자동 매매 전략 정의 및 매니저 기반 다중 전략 관리
- **실전 예제 제공 (`examples.py`)**: API 활용법 및 주요 유스케이스 예제 포함
- **터미널 포맷터 (`utils/printer.py`)**: 가독성 높은 CLI 데이터 출력 지원

---

## 📂 프로젝트 구조 (Project Structure)

```bash
TossAutoTradingSystem/
├── models/                  # Pydantic 기반 API 응답 / 요청 데이터 모델
│   ├── account.py           # 계좌 및 잔고 모델
│   ├── candles.py           # 차트/캔들 데이터 모델
│   ├── exchange_rate.py     # 환율 정보 모델
│   ├── korea_market.py      # 국내 시장 정보 모델
│   ├── market_session.py    # 장 상태/세션 모델
│   ├── order.py             # 주문 요청/응답 모델
│   ├── orderbook.py         # 호가 잔량 모델
│   ├── price.py             # 시세/현재가 모델
│   ├── price_limit.py       # 상/하한가 모델
│   ├── trades.py            # 체결 내역 모델
│   └── us_market.py         # 미국 시장 정보 모델
├── utils/                   # 공통 유틸리티
│   └── printer.py           # 터미널 결과 포맷팅 및 출력
├── account.py               # 계좌/잔고 API 서비스
├── auth.py                  # API Key / OAuth 인증 및 토큰 관리
├── base.py                  # HTTP 요청 Base Client
├── client.py                # 메인 통합 TossClient 엔트리포인트
├── config.py                # 설정 및 환경변수 관리
├── endpoints.py             # API Endpoint URL 상주 관리
├── enums.py                 # 매수/매도, 주문 유형 등 Enum 정의
├── examples.py              # 종합 사용 예제 (계좌, 시세, 주문, 전략)
├── exceptions.py            # 커스텀 에러 핸들러
├── market.py                # 주식 시세, 캔들, 호가 조회 서비스
├── market_info.py           # 시장 세션 및 세부정보 서비스
├── order.py                 # 주문 매수/매도/취소 서비스
├── order_id.py              # 주문 UUID 생성기
├── stratege_manager.py      # 전략 관리 및 매니저 실행 엔진
├── strategies.py            # 사용자 정의 매매 전략 모음
├── strategy.py              # 기본 Strategy 추상 클래스
└── requirements.txt         # 의존성 모듈 목록
```

---

## ⚙️ 설치 방법 (Installation)

### 1. 저장소 클론 (master 브랜치)
```bash
git clone https://github.com/your-repo/TossAutoTradingSystem.git
cd TossAutoTradingSystem
```

### 2. 가상환경 및 패키지 설치
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 빠른 시작 (Quick Start)

### 1. 환경 변수 설정 (`.env`)
 프로젝트 루트 디렉터리에 `.env` 파일을 생성하거나 `config.py`에 키를 입력합니다.

```env
TOSS_API_KEY=your_api_key_here
TOSS_SECRET_KEY=your_secret_key_here
TOSS_ACCOUNT_NO=your_account_number
```

---

## 💡 예제 파일 (`examples.py`) 활용법

master 브랜치에 추가된 `examples.py`에는 주요 기능별 실전 활용 코드 모음이 포함되어 있습니다.

### 1. 전체 예제 실행하기
```bash
python examples.py
```

### 2. 주요 기능 코드 미리보기

#### ① 계좌 정보 및 잔고 조회
```python
from client import TossClient

client = TossClient()

# 계좌 상태 및 잔고 조회
account_summary = client.account.get_summary()
print(f"예수금: {account_summary.balance:,}원")

for pos in account_summary.positions:
    print(f"종목: {pos.symbol} | 수량: {pos.quantity}주 | 평가금액: {pos.eval_amount:,}원")
```

#### ② 시세 & 캔들 데이터 조회 (`market.py`)
```python
from client import TossClient

client = TossClient()

# 1분봉 캔들 조회 (삼성전자 예시)
candles = client.market.get_candles(symbol="005930", timeframe="1m", count=10)
for c in candles:
    print(f"시간: {c.timestamp} | 시가: {c.open} | 종가: {c.close} | 거래량: {c.volume}")

# 현재 호가 조회
orderbook = client.market.get_orderbook(symbol="005930")
print(f"최우선 매도호가: {orderbook.asks[0].price}원 | 매수호가: {orderbook.bids[0].price}원")
```

#### ③ 주문 생성 및 취소 (`order.py`)
```python
from client import TossClient
from enums import Side, OrderType

client = TossClient()

# 지정가 매수 주문
order = client.order.create_order(
    symbol="005930",
    qty=5,
    price=71000,
    side=Side.BUY,
    order_type=OrderType.LIMIT
)
print(f"주문 완료 - Order ID: {order.order_id}")

# 미체결 주문 취소
client.order.cancel_order(order_id=order.order_id)
```

#### ④ 트레이딩 전략 자동화 (`stratege_manager.py`)
```python
from stratege_manager import StrategyManager
from strategies import SimpleMovingAverageStrategy

manager = StrategyManager()
manager.add_strategy(SimpleMovingAverageStrategy(symbol="005930", short_window=5, long_window=20))

# 자동 매매 루프 실행
manager.run()
```

---

## 🛠 주요 모듈 가이드

| 모듈명 | 주요 기능 및 역할 |
| :--- | :--- |
| **`client.py`** | 토스증권 API 통합 엔트리포인트 (`account`, `market`, `order` 통합) |
| **`market.py` / `market_info.py`** | 주식 캔들 차트, 현재가, 체결 내역, 호가 잔량 및 시장 세션 조회 |
| **`order.py`** | 신규 주문(매수/매도), 잔여 주문 취소 및 체결 내역 조회 |
| **`stratege_manager.py`** | 등록된 전략을 주기적으로 평가하고 자동 주문을 실행하는 관리자 |
| **`examples.py`** | 시세 조회, 계좌 조회, 주문 및 전략 실행을 위한 종합 가이드 코드 |
| **`models/`** | Pydantic/Dataclass 기반 구조화된 응답 객체 모음 |

---

## ⚠️ 주의사항

- 본 프로젝트는 **실전 주식 매매**에 사용되므로 API Key와 Secret이 외부로 유출되지 않도록 주의하세요.
- 자동매매 전략 실행 전 모의 환경이나 소액으로 반드시 검증을 진행하십시오.

---

## 📄 라이선스 (License)

Distributed under the MIT License. See `LICENSE` for more information.
