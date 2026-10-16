# Test cases for payment-functions.yml. This file is a fixture and is never imported.
import stripe


def checkout(order, payments, gateway, battery, params: dict) -> None:
    key = f"order-{order.id}"

    # ruleid: payment-call-idempotency-key-required
    payments.charge(order.customer, order.total)
    # ruleid: payment-call-idempotency-key-required
    gateway.create_payment(amount=order.total)
    # ruleid: payment-call-idempotency-key-required
    gateway.capture_payment(order.payment_id)
    # ruleid: payment-call-idempotency-key-required
    refund_order(order)
    # ruleid: payment-call-idempotency-key-required
    payments.pay_invoice(order.invoice_id)
    # ruleid: payment-call-idempotency-key-required
    gateway.initiate_transfer(order.seller, order.total)
    # ruleid: payment-call-idempotency-key-required
    payout(order.seller)

    # ok: payment-call-idempotency-key-required
    payments.charge(order.customer, order.total, idempotency_key=key)
    # ok: payment-call-idempotency-key-required
    refund_order(order, idempotency_key=f"refund-{order.id}")
    # ok: payment-call-idempotency-key-required
    gateway.create_payment(**params)
    # ok: payment-call-idempotency-key-required
    gateway.refund_status(order.payment_id)
    # ok: payment-call-idempotency-key-required
    gateway.payment_id(order)
    # ok: payment-call-idempotency-key-required
    payments.charge_amount(order)
    # ok: payment-call-idempotency-key-required
    gateway.transfer(order)
    # ok: payment-call-idempotency-key-required
    gateway.get_payment(order.payment_id)
    # ok: payment-call-idempotency-key-required
    battery.recharge()
    # ok: payment-call-idempotency-key-required
    payments.payment_methods(order.customer)
    # ok: payment-call-idempotency-key-required
    stripe.Charge.capture("ch_123")


# ok: payment-call-idempotency-key-required
def charge(customer, amount, idempotency_key: str) -> None: ...
