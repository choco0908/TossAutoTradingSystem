# 📈 TossAutoTradingSystem

> **토스증권 API 기반의 파이썬 자동매매 SDK 및 시스템**
>
> 토스증권 API를 쉽고 안전하게 활용하여 계좌 조회, 주문(매수/매도), 잔고 관리, 주문 내역 조회를 자동화할 수 있는 Python 클라이언트 라이브러리입니다.

---

## 📸 Overview

`TossAutoTradingSystem`은 토스증권 API 인증 및 각 엔드포인트 간의 통신을 모듈화하여 단순하고 직관적인 인터페이스를 제공합니다.

- **인증 토큰 자동 관리 및 갱신** (`auth.py`, `config.py`)
- **계좌/잔고 조회 및 분석** (`account.py`, `models/account.py`)
- **매수 / 매도 주문 실행 및 취소** (`order.py`, `models/order.py`)
- **상태/타입 모듈화** (`enums.py`, `endpoints.py`, `exceptions.py`)
- **출력 및 유틸리티 지원** (`utils/printer.py`)

---

## 📂 프로젝트 구조 (Project Structure)

```bash
TossAutoTradingSystem/
├── models/                  # 데이터 응답 객체 (Pydantic / Dataclass 기반 모델)
│   ├── __init__.py
│   ├── account.py           # 계좌 및 잔고 데이터 모델
│   └── order.py             # 주문 요청/응답 데이터 모델
├── utils/                   # 공통 유틸리티
│   └── printer.py           # 터미널 가독성 향상 포맷터/프린터
├── __init__.py              # 모듈 초기화
├── account.py               # 계좌 관련 API 호출 서비스
├── account_example.py       # 계좌 조회 예제 코드
├── auth.py                  # OAuth / API Key 인증 처리
├── base.py                  # Base API Client (HTTP 통신 공통 모듈)
├── client.py                # 토스증권 메인 통합 클라이언트
├── config.py                # 설정 및 환경 변수 관리
├── endpoints.py             # API 엔드포인트 URL 정의
├── enums.py                 # 매수/매도, 주문유형 등 Enum 모음
├── exceptions.py            # API 에러 핸들링 Custom Exception
├── order.py                 # 주문 생성 및 관리 서비스
├── order_id.py              # 주문 ID 생성 및 추적 유틸리티
└── requirements.txt         # 의존성 패키지 목록
```

---

## ⚙️ 설치 방법 (Installation)

### 1. Repository 클론
```bash
git clone https://github.com/your-repo/TossAutoTradingSystem.git
cd TossAutoTradingSystem
```

### 2. 가상환경 구성 및 의존성 설치
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 빠른 시작 (Quick Start)

### 1. 환경변수 설정 (`.env` 또는 `config.py`)
토스증권 API 사용을 위해 발급받은 API Key 및 계좌 정보를 설정합니다.

```env
TOSS_API_KEY=your_api_key_here
TOSS_SECRET_KEY=your_secret_key_here
TOSS_ACCOUNT_NO=your_account_number
```

### 2. 계좌 조회 예제
`account_example.py` 실행 또는 아래 예제 코드를 사용해 계좌 상태를 확인하세요.

```python
from client import TossClient

# 클라이언트 초기화
client = TossClient()

# 계좌 예수금 및 보유 잔고 조회
account_info = client.account.get_summary()

print(f"총 예수금: {account_info.balance:,}원")
print("보유 종목:")
for position in account_info.positions:
    print(f"- {position.stock_name} ({position.symbol}): {position.quantity}주")
```

### 3. 주식 주문 예제 (`order.py`)

```python
from client import TossClient
from enums import OrderType, Side

client = TossClient()

# 지정가 매수 주문
order_response = client.order.create_order(
    symbol="005930",       # 삼성전자
    qty=10,                # 10주
    price=70000,           # 70,000원
    side=Side.BUY,         # 매수
    order_type=OrderType.LIMIT  # 지정가
)

print(f"주문 완료 - Order ID: {order_response.order_id}")
```

---

## 🛠 주요 모듈 상세 가이드

| 모듈 | 역할 및 기능 설명 |
| :--- | :--- |
| **`client.py`** | 토스증권 API 통합 엔트리포인트 (`account`, `order` 기능 통합) |
| **`auth.py`** | 토스증권 API 인증 헤더 생성 및 토큰 주기적 갱신 |
| **`account.py`** | 계좌 내 예수금, 총 자산, 보유 주식 잔고 조회 |
| **`order.py`** | 신규 주문(매수/매도), 잔여 주문 취소, 체결 내역 조회 |
| **`models/`** | API 응답 데이터를 파이썬 객체로 파싱 및 검증 |
| **`exceptions.py`** | API 응답 상태 코드에 따른 커스텀 예외 처리 모듈 |

---

## ⚠️ 주의사항 (Notice)

- 본 라이브러리는 **실제 투자 및 매매**에 사용되므로 API 키 및 개인 계좌 정보가 외부에 노출되지 않도록 `.gitignore` 관리 및 환경변수 사용을 권장합니다.
- 토스증권 API 서비스의 점검 시간 및 가이드라인을 반드시 준수하세요.

---

## 📄 라이선스 (License)

Distributed under the MIT License. See `LICENSE` for more information.
