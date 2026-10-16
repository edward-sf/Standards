from decimal import Decimal

from app.money import add_tax


def test_add_tax_rounds_to_pennies() -> None:
    assert add_tax(Decimal("19.99"), Decimal("0.2")) == Decimal("23.99")
