# Test cases for money-rules.yml. Run: bash semgrep/semgrep.sh --test semgrep/
# This file is a fixture and is never imported.
import decimal
import logging
from decimal import Decimal
from typing import Optional

logger = logging.getLogger(__name__)


# --- no-float-for-money ---

# ruleid: no-float-for-money
def charge(order_id: str, amount: float) -> None: ...


# ruleid: no-float-for-money
def refund(order_id: str, refund_amount: float = 0.0) -> None: ...


# ruleid: no-float-for-money
def order_total(items: list[str]) -> float: ...


class Invoice:
    # ruleid: no-float-for-money
    subtotal: float
    # ruleid: no-float-for-money
    tax: Optional[float]
    # ruleid: no-float-for-money
    discount_amount: float | None = None

    def load(self, raw: str) -> None:
        # ruleid: no-float-for-money
        self.balance = float(raw)


# ruleid: no-float-for-money
price = float("19.99")

# ok: no-float-for-money
amount = Decimal("19.99")
# ok: no-float-for-money
amount_cents: int = 1999
# ok: no-float-for-money
tax_rate: float = 0.2
# ok: no-float-for-money
fee_percent: float = 2.9
# ok: no-float-for-money
latency: float = 0.5


# ok: no-float-for-money
def conversion_rate(base: str, quote: str) -> float: ...


# --- no-decimal-from-float ---

# ruleid: no-decimal-from-float
a = Decimal(0.1)
# ruleid: no-decimal-from-float
b = decimal.Decimal(19.99)
# ruleid: no-decimal-from-float
c = Decimal(float(price))
# ok: no-decimal-from-float
d = Decimal("0.1")
# ok: no-decimal-from-float
e = Decimal(10)


# --- no-logging-card-numbers ---

def log_payment(card_number: str, card, pan: str, cvv: str, card_last4: str, token: str) -> None:
    # ruleid: no-logging-card-numbers
    logger.info("charging card %s", card_number)
    # ruleid: no-logging-card-numbers
    logger.debug(f"card={card.number}, pan={pan}")
    # ruleid: no-logging-card-numbers
    logging.error("declined", extra={"cvv": cvv})
    # ruleid: no-logging-card-numbers
    logger.warning("retrying", card_no=card_number)
    # ruleid: no-logging-card-numbers
    print("card", pan)

    # ok: no-logging-card-numbers
    logger.info("charging card ending %s", card_last4)
    # ok: no-logging-card-numbers
    logger.info("charging card token %s", token)
    # ok: no-logging-card-numbers
    logger.info("charging card", extra={"card_token": token})
    # ok: no-logging-card-numbers
    logger.info("panel opened")
    # ok: no-logging-card-numbers
    logger.info("company=%s", "Acme")
