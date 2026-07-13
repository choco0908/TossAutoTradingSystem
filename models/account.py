"""
tossinvest.models.account

Account Models
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class Account:
    """
    Investment account.
    """

    account_seq: str
    account_number: str = ""
    account_name: str = ""
    account_type: str = ""
    status: str = ""
    currency: str = "KRW"

    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "Account":

        return cls(
            account_seq=data.get("accountSeq", ""),
            account_number=data.get("accountNumber", ""),
            account_name=data.get("accountName", ""),
            account_type=data.get("accountType", ""),
            status=data.get("status", ""),
            currency=data.get("currency", "KRW"),
            raw=data,
        )


@dataclass(slots=True)
class Holding:
    """
    Holding asset.
    """

    market: str
    symbol: str
    name: str

    quantity: float

    available_quantity: float = 0

    average_price: float = 0

    current_price: float = 0

    evaluation_amount: float = 0

    purchase_amount: float = 0

    profit_loss: float = 0

    profit_loss_rate: float = 0

    currency: str = ""

    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "Holding":

        return cls(
            market=data.get("market", ""),
            symbol=data.get("symbol", ""),
            name=data.get("name", ""),
            quantity=float(data.get("quantity", 0)),
            available_quantity=float(
                data.get(
                    "availableQuantity",
                    data.get("quantity", 0),
                )
            ),
            average_price=float(
                data.get(
                    "averagePrice",
                    0,
                )
            ),
            current_price=float(
                data.get(
                    "currentPrice",
                    0,
                )
            ),
            evaluation_amount=float(
                data.get(
                    "evaluationAmount",
                    0,
                )
            ),
            purchase_amount=float(
                data.get(
                    "purchaseAmount",
                    0,
                )
            ),
            profit_loss=float(
                data.get(
                    "profitLoss",
                    0,
                )
            ),
            profit_loss_rate=float(
                data.get(
                    "profitLossRate",
                    0,
                )
            ),
            currency=data.get("currency", ""),
            raw=data,
        )


@dataclass(slots=True)
class AccountBalance:
    """
    Account balance summary.
    """

    cash: float = 0

    withdrawable_cash: float = 0

    buying_power: float = 0

    total_asset: float = 0

    total_purchase_amount: float = 0

    total_evaluation_amount: float = 0

    total_profit_loss: float = 0

    total_profit_loss_rate: float = 0

    currency: str = ""

    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "AccountBalance":

        return cls(
            cash=float(data.get("cash", 0)),
            withdrawable_cash=float(
                data.get(
                    "withdrawableCash",
                    0,
                )
            ),
            buying_power=float(
                data.get(
                    "buyingPower",
                    0,
                )
            ),
            total_asset=float(
                data.get(
                    "totalAsset",
                    0,
                )
            ),
            total_purchase_amount=float(
                data.get(
                    "totalPurchaseAmount",
                    0,
                )
            ),
            total_evaluation_amount=float(
                data.get(
                    "totalEvaluationAmount",
                    0,
                )
            ),
            total_profit_loss=float(
                data.get(
                    "totalProfitLoss",
                    0,
                )
            ),
            total_profit_loss_rate=float(
                data.get(
                    "totalProfitLossRate",
                    0,
                )
            ),
            currency=data.get("currency", ""),
            raw=data,
        )


@dataclass(slots=True)
class HoldingsResponse:
    """
    Holdings response.
    """

    holdings: List[Holding] = field(default_factory=list)

    balance: Optional[AccountBalance] = None

    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "HoldingsResponse":

        holdings_data = (
            data.get("holdings")
            or data.get("results")
            or data.get("items")
            or []
        )

        holdings = [
            Holding.from_dict(item)
            for item in holdings_data
        ]

        balance = None

        if "balance" in data:
            balance = AccountBalance.from_dict(
                data["balance"]
            )

        return cls(
            holdings=holdings,
            balance=balance,
            raw=data,
        )