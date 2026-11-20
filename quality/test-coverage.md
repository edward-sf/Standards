# Test coverage

Use coverage to locate behavior that needs investigation during change review. Projects choose their own measured code and thresholds. A small change to error handling can deserve targeted tests even in a well-covered package.

## Interpret the report

For the reservation endpoint in the [testing strategy](testing-strategy.md), an integration test may execute every line of the conflict handler and only assert that a response exists. Replacing 409 with 500 then leaves the test green. Exercise that change temporarily and observe the result. A test that asserts the exact public status should fail. Restore the handler and verify it passes. Also check the database postcondition if the change can commit partial writes.

The reviewer SHOULD examine the changed branches, excluded files, and failure assertions when deciding if coverage is meaningful. A changed-line metric can point to unexecuted code. Neither a line count nor the presence of an assertion can decide whether 409 is the promised result.

## Enforce a client threshold

When a client adopts a minimum line-coverage percentage, its maintainer MUST block merge if the measured fraction falls below the configured floor or the required report is missing or invalid. Set the threshold in protected policy. Generate fresh Cobertura XML with the client's chosen source scope on the candidate revision and preserve the measurement command's exit status. Pass it to the [same required CI check](../checks/quality/test_reports.py) as the test reports.

```sh
python3 "$STANDARDS/checks/quality/test_reports.py" build/tests.xml \
  --case ReservationAPI::duplicate_seat_returns_conflict \
  --coverage build/coverage.xml --minimum 80
```

A report with 4 covered lines out of 5 passes an 80 percent floor. Three out of five blocks. A zero denominator cannot establish a measured percentage. Clients without a numeric policy omit both coverage arguments and still verify required test cases. Reviewers decide whether the measurement scope and assertions cover the risk.
