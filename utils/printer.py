"""
tossinvest.utils.printer

Pretty printer using Rich
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


# ----------------------------------------------------------------------
# Generic
# ----------------------------------------------------------------------


def print_json(data: Any) -> None:
    """
    Pretty JSON
    """

    console.print_json(
        json.dumps(
            data,
            ensure_ascii=False,
            default=str,
        )
    )


def print_panel(
        title: str,
        text: str,
) -> None:
    console.print(
        Panel.fit(
            text,
            title=title,
        )
    )


# ----------------------------------------------------------------------
# Accounts
# ----------------------------------------------------------------------


def print_accounts(accounts: List[Dict[str, Any]]) -> None:
    table = Table(
        title="Accounts",
        show_lines=True,
    )

    table.add_column("Seq", style="cyan")
    table.add_column("Account")
    table.add_column("Type")
    table.add_column("Currency")
    table.add_column("Status")

    for account in accounts:
        table.add_row(
            str(account.get("accountSeq", "")),
            account.get("accountNo", ""),
            account.get("accountType", ""),
            account.get("currency", ""),
            account.get("status", ""),
        )

    console.print(table)


# ----------------------------------------------------------------------
# Holdings
# ----------------------------------------------------------------------


def print_holdings(items: List[Dict[str, Any]], market: str = None) -> None:
    table = Table(
        title="Portfolio",
        show_lines=True,
    )

    table.add_column("Market")
    table.add_column("Symbol", style="cyan")
    table.add_column("Name")
    table.add_column("Qty", justify="right")
    table.add_column("Avg", justify="right")
    table.add_column("Current", justify="right")
    table.add_column("PnL", justify="right")
    table.add_column("PnL %", justify="right")

    if market is not None:
        for item in items:
            if market == item.get("marketCountry", ""):
                table.add_row(
                    item.get("marketCountry", ""),
                    item.get("symbol", ""),
                    item.get("name", ""),
                    str(item.get("quantity", "")),
                    f'{float(item.get("averagePurchasePrice", 0)):,.2f}',
                    f'{float(item.get("lastPrice", 0)):,.2f}',
                    f'{float(item.get("profitLoss").get("amountAfterCost",0)):,.2f}',
                    f'{float(item.get("profitLoss").get("rateAfterCost",0)) * 100:,.2f}%',
                )
    else:
        for item in items:
            table.add_row(
                item.get("marketCountry", ""),
                item.get("symbol", ""),
                item.get("name", ""),
                str(item.get("quantity", "")),
                f'{float(item.get("averagePurchasePrice", 0)):,.2f}',
                f'{float(item.get("lastPrice", 0)):,.2f}',
                f'{float(item.get("profitLoss").get("amountAfterCost", 0)):,.2f}',
                f'{float(item.get("profitLoss").get("rateAfterCost", 0) * 100):,.2f}%',
            )

    console.print(table)

# ----------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------

def print_summary(summary: Dict[str, Any]) -> None:
    """
    계좌 평가금액 출력
    """

    table = Table(
        title="Portfolio Summary",
        show_lines=True,
    )

    table.add_column("Item")
    table.add_column("KRW", justify="right")
    table.add_column("USD", justify="right")

    purchase = summary.get("totalPurchaseAmount", {})
    market = summary.get("marketValue", {}).get("amount", {})
    market_after = summary.get("marketValue", {}).get("amountAfterCost", {})
    profit = summary.get("profitLoss", {}).get("amount", {})
    profit_after = summary.get("profitLoss", {}).get("amountAfterCost", {})
    daily = summary.get("dailyProfitLoss", {}).get("amount", {})

    table.add_row(
        "Purchase",
        f"{int(purchase.get('krw', 0)):,}",
        f"{float(purchase.get('usd', 0)):,.2f}",
    )

    table.add_row(
        "Market Value",
        f"{int(market.get('krw', 0)):,}",
        f"{float(market.get('usd', 0)):,.2f}",
    )

    table.add_row(
        "After Cost",
        f"{int(market_after.get('krw', 0)):,}",
        f"{float(market_after.get('usd', 0)):,.2f}",
    )

    table.add_row(
        "Profit",
        f"{int(profit.get('krw', 0)):,}",
        f"{float(profit.get('usd', 0)):,.2f}",
    )

    table.add_row(
        "Profit After Cost",
        f"{int(profit_after.get('krw', 0)):,}",
        f"{float(profit_after.get('usd', 0)):,.2f}",
    )

    table.add_row(
        "Today",
        f"{int(daily.get('krw', 0)):,}",
        f"{float(daily.get('usd', 0)):,.2f}",
    )

    console.print(table)

# ----------------------------------------------------------------------
# Orders
# ----------------------------------------------------------------------


def print_orders(orders: List[Dict[str, Any]]) -> None:
    table = Table(
        title="Orders",
        show_lines=True,
    )

    table.add_column("Order ID")
    table.add_column("Market")
    table.add_column("Symbol")
    table.add_column("Side")
    table.add_column("Type")
    table.add_column("Qty", justify="right")
    table.add_column("Filled", justify="right")
    table.add_column("Price", justify="right")
    table.add_column("Status")

    for order in orders:
        table.add_row(
            str(order.get("orderId", "")),
            order.get("market", ""),
            order.get("symbol", ""),
            order.get("side", ""),
            order.get("orderType", ""),
            str(order.get("quantity", "")),
            str(order.get("filledQuantity", "")),
            f'{float(order.get("price", 0)):,.2f}',
            order.get("status", ""),
        )

    console.print(table)


# ----------------------------------------------------------------------
# Rankings
# ----------------------------------------------------------------------


def print_rankings(items: List[Dict[str, Any]]) -> None:
    table = Table(
        title="Rankings",
        show_lines=True,
    )

    table.add_column("Rank")
    table.add_column("Symbol", style="cyan")
    table.add_column("Name")
    table.add_column("Price", justify="right")
    table.add_column("Change %", justify="right")
    table.add_column("Volume", justify="right")

    for idx, item in enumerate(items, start=1):
        table.add_row(
            str(idx),
            item.get("symbol", ""),
            item.get("name", ""),
            f'{float(item.get("price", 0)):,.2f}',
            f'{float(item.get("changeRate", 0)):,.2f}%',
            f'{int(item.get("volume", 0)):,}',
        )

    console.print(table)


# ----------------------------------------------------------------------
# Market Price
# ----------------------------------------------------------------------


def print_quote(data: Dict[str, Any]) -> None:
    table = Table(
        title="Quote",
        show_lines=True,
    )

    table.add_column("Field")
    table.add_column("Value")

    for key, value in data.items():
        table.add_row(
            str(key),
            str(value),
        )

    console.print(table)


# ----------------------------------------------------------------------
# Auto
# ----------------------------------------------------------------------


def pprint(data: Any) -> None:
    """
    Automatically choose the best output format.
    """

    if isinstance(data, dict):

        if "holdings" in data:
            print_holdings(data)
            return

        print_json(data)
        return

    if isinstance(data, list):

        if not data:
            console.print("[yellow]No Data[/yellow]")
            return

        first = data[0]

        if isinstance(first, dict):

            if "accountSeq" in first:
                print_accounts(data)
                return

            if "orderId" in first:
                print_orders(data)
                return

            if "symbol" in first:
                print_rankings(data)
                return

        print_json(data)
        return

    console.print(data)
