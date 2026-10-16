from decimal import ROUND_HALF_EVEN, Decimal


def add_tax(amount: Decimal, tax_rate: Decimal) -> Decimal:
    total = amount * (1 + tax_rate)
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
