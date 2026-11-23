# Testing strategy

Use this standard when a change alters behavior or fixes a regression. The author chooses the cheapest test that can observe the failure. The client maintainer configures the checks that protect merge.

## Choose the boundary

Consider an API that creates a reservation in a datastore. A second request for the same seat should receive a conflict response.

| Level | Exercise | Failure it catches |
| --- | --- | --- |
| Unit | Give the service a fake repository that reports a duplicate. Assert the service returns the domain conflict. | A handler treats a duplicate as success. |
| Integration | Insert the same seat twice against the database engine and schema used by the service. Assert one row remains and the adapter translates the constraint violation. | A fake repository hides a missing unique constraint or a driver-specific error. |
| End to end | Start the application with an isolated database. Send two requests through its HTTP entry point. Assert 201 then 409, and check the first reservation still exists. | Middleware translates the correct domain error into HTTP 500. |

Group tests by feature and boundary. Name the observable outcome, for example `duplicate_seat_returns_conflict`. Give each run its own schema or transaction and synthetic records. Freeze or inject the clock where timing matters. Use a fake to force a rare error and a real adapter test to check that the fake represents the boundary. A test that passes only after another test seeds a seat needs its own fixture.

For a regression, the author SHOULD reproduce the reported behavior against the affected revision, retain the failing assertion, and show it passing on the fix. If reproducing an incident would require production data, record the limitation and test the nearest safe boundary with synthetic data.

## Gate the change

A subscribing maintainer MUST require the configured suites to succeed on the revision being merged and the named regression or contract cases to run and pass. Keep the list of required cases in reviewed CI policy. The author supplies the cases and the reviewer checks whether they exercise the changed behavior.

Run the native test runner in a clean workspace and preserve its exit status. Generate fresh JUnit XML for the required suites in that job. Make successful completion of the runner **and** the [report check](../checks/quality/test_reports.py) required for merge. Supply one or more report files and at least one required case as `classname::name`. Use a pinned Standards revision and protected CI policy for the gate. A report from another revision or a PR attachment is insufficient evidence.

```sh
python3 "$STANDARDS/checks/quality/test_reports.py" build/unit.xml build/integration.xml build/http.xml \
  --case ReservationAPI::duplicate_seat_returns_conflict
```

A missing or skipped required case blocks merge even when the runner returns success. A failure or error anywhere in the supplied reports also blocks. The checker cannot distinguish a fake datastore from a real one by test name. A reviewer inspects the fixture setup, isolation and assertions. Renaming a mock-based test to include “integration” leaves its dependencies unchanged. The [coverage standard](test-coverage.md) describes a second check on the same evidence.
