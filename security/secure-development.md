# Secure development

Use this standard when a change affects an identity, an access decision or the handling of sensitive data. The worked example is a customer record read. Apply the same reasoning to other operations and include state-change assertions for writes.

## Review a protected operation

A change adds a display name to an authenticated customer endpoint. The author traces the request from credential validation through authorization, storage, serialization and logging. The service should derive the caller's identity from the verified session, scope its parameterized lookup to records the caller may read, and construct the public response from approved fields. Design the error response to avoid exposing another customer's data. Keep credentials and sensitive fields out of diagnostics. Limit retained data and log access to the service's operational needs.

A signed-in caller can still request a record belonging to another account. Use two distinct synthetic principals and a record with distinguishable public and private values. Include a successful owner read so a server that denies every request cannot pass. Review changes to session validation, tenant boundaries, privileges, response fields or log destinations with someone familiar with the affected trust boundary. Apply the client's [review policy](../development/code-review.md) to the revision being merged.

## Gate protected reads

For each protected read covered by the client policy, its maintainer MUST gate merge on fresh observations of an authorized read, an anonymous read, a request with invalid credentials, and an authenticated read outside the caller's authorization. The author supplies integration fixtures. The reviewer approves the expected status and public JSON body for each case. The client MUST reject a contract mismatch or the appearance of the fixture's private sentinel in captured application logs.

Run the client integration harness in an isolated environment at the candidate revision. Create actual requests against the application entry point. Collect the parsed JSON response and HTTP status for each case, and capture the application log stream from startup through flush. Include a known non-sensitive correlation marker emitted by the fixture request so selecting an empty or unrelated log fails. Generate fresh artifacts in a clean CI job and preserve the harness exit status. Keep expectations and fixture configuration under trusted review independently of generated observations.

Use the [Standards check](../checks/security/read_contract.py) once per covered operation in a required merge job. Supply the reviewed expectations, the harness observations, the captured UTF-8 log, and two distinct synthetic markers. Both JSON files are objects with exactly the four case names below. Each case contains an integer `status` and a `body` containing the entire parsed public response. Choose denial responses appropriate for the API, including 404 when the contract conceals resource existence.

| Fixture case | Expected response for this endpoint |
| --- | --- |
| owner | 200 and `{"id":"fixture-a","display_name":"Ada"}` |
| anonymous | 401 and `{"error":"unauthenticated"}` |
| invalid | 401 and the same public error |
| other | 404 and `{"error":"not_found"}` |

```sh
python3 "$STANDARDS/checks/security/read_contract.py" policy/read-customer.json \
  build/read-customer.json build/application.log \
  --private-marker FIXTURE_PRIVATE_73 --log-marker FIXTURE_REQUEST_92
```

If the other principal receives 200, or the owner response starts exposing an internal field, CI blocks merge. Repeat the cases after repairing the query or serializer. Preserve redacted results and the revision with the PR.

## Review the remaining risk

Comparing complete fixture responses catches additional fields. Checking for the literal sentinel in the captured log catches that value on the exercised path. Neither establishes how an alternate role, an unexercised route, an encoded value or a separate telemetry sink behaves. Searching source for an authorization decorator also misses a correctly decorated endpoint whose query uses the wrong tenant. The reviewer inspects the access model, fixture identities, route inventory, data classification, relevant sinks and failure paths to decide which further cases and controls the change needs.

See the [OWASP authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).
