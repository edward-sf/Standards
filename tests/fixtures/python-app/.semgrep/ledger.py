# Test cases for ledger.yml. This file is a fixture and is never imported.


def settle(ledger, self_ledger, http, key):
    # ruleid: ledger-post-idempotency-key-required
    ledger.post("acct_1", 100)
    # ruleid: ledger-post-idempotency-key-required
    self_ledger.post("acct_1", 100)
    # ok: ledger-post-idempotency-key-required
    ledger.post("acct_1", 100, idempotency_key=key)
    # ok: ledger-post-idempotency-key-required
    http.post("/ledger", json={})
