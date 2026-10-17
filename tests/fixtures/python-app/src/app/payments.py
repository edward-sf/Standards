from decimal import Decimal
from typing import Protocol


class Ledger(Protocol):
    def post(self, account: str, amount: Decimal, *, idempotency_key: str) -> None: ...


class Gateway(Protocol):
    def charge(
        self, customer_id: str, amount: Decimal, *, idempotency_key: str
    ) -> str: ...


def checkout(
    gateway: Gateway, ledger: Ledger, order_id: str, customer_id: str, amount: Decimal
) -> str:
    key = f"order-{order_id}"
    payment_id = gateway.charge(customer_id, amount, idempotency_key=key)
    ledger.post(customer_id, amount, idempotency_key=key)
    return payment_id
