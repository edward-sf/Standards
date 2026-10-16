# Test cases for stripe.yml. This file is a fixture and is never imported.
import stripe


def pay(order_id: str, client: stripe.StripeClient, opts: dict) -> None:
    key = f"order-{order_id}"

    # ruleid: stripe-idempotency-key-required
    stripe.PaymentIntent.create(amount=1999, currency="gbp")
    # ruleid: stripe-idempotency-key-required
    stripe.Refund.create(payment_intent="pi_123")
    # ruleid: stripe-idempotency-key-required
    client.payment_intents.create(params={"amount": 1999, "currency": "gbp"})
    # ruleid: stripe-idempotency-key-required
    client.v1.refunds.create(params={"payment_intent": "pi_123"}, options={"stripe_account": "acct_1"})

    # ok: stripe-idempotency-key-required
    stripe.PaymentIntent.create(amount=1999, currency="gbp", idempotency_key=key)
    # ok: stripe-idempotency-key-required
    client.payment_intents.create(params={"amount": 1999}, options={"idempotency_key": key})
    # ok: stripe-idempotency-key-required
    client.v1.refunds.create(params={"payment_intent": "pi_123"}, options={"stripe_account": "acct_1", "idempotency_key": key})
    # ok: stripe-idempotency-key-required
    client.payouts.create(params={"amount": 500}, options=opts)
    # ok: stripe-idempotency-key-required
    stripe.PaymentIntent.retrieve("pi_123")
    # ok: stripe-idempotency-key-required
    client.customers.create(params={"email": "a@example.com"})
