from decimal import Decimal

from app.payments import checkout


class FakeGateway:
    def __init__(self) -> None:
        self.keys: list[str] = []

    def charge(self, customer_id: str, amount: Decimal, *, idempotency_key: str) -> str:
        self.keys.append(idempotency_key)
        return "pay_1"


class FakeLedger:
    def __init__(self) -> None:
        self.keys: list[str] = []

    def post(self, account: str, amount: Decimal, *, idempotency_key: str) -> None:
        self.keys.append(idempotency_key)


def test_checkout_uses_one_key_per_order() -> None:
    gateway, ledger = FakeGateway(), FakeLedger()
    assert checkout(gateway, ledger, "42", "cus_1", Decimal("9.99")) == "pay_1"
    assert gateway.keys == ledger.keys == ["order-42"]
