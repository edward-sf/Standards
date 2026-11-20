# Project documentation

Use this standard to decide what a user, contributor or operator needs to know after a change. The maintainer owns the entry points and publishes their locations in the repository.

## Follow a public API change

A reservations API adds an optional page token. The author updates the API reference with the request parameter, its default, the response field and the error returned for an invalid token. The README still needs to get a new user from setup to one working request. Update its example if the first request changed. Keep an inline comment beside the cursor comparison if it explains a non-obvious ordering constraint. A comment repeating each statement will go stale without helping the next maintainer.

Add a changelog entry describing the caller-visible change. At release, the release author SHOULD turn applicable entries into notes that identify the version, impact, migration steps and any required action. For this backward-compatible addition, existing callers can continue their first-page request. If a later version removes offset pagination, explain how to migrate and when the old parameter stops working. Use an [ADR](adr-standards.md) when choosing or changing a consequential design.

## Check documentation on the candidate revision

The client maintainer MUST require a nonempty README at its configured path. When a published API contract file matches the configured path patterns and changes, the author MUST update the configured API reference and changelog. Point the patterns at published contract definitions, such as a schema or versioned interface file. Keep the three documentation files distinct. Projects whose schema generates the reference can commit the regenerated reference or configure the gate around the reviewed source of the reference, with a distinct contract input.

Run the [documentation check](../checks/documentation/docs_gate.py) in the required merge job with the base and candidate Git revisions. Fetch both histories, use the actual integration candidate and take paths, patterns and the Standards revision from protected policy. Use repository-relative, case-sensitive paths. The checker reads files at the candidate commit and examines changes since its merge base. Deleting a contract is also a public change.

```sh
python3 "$STANDARDS/checks/documentation/docs_gate.py" "$BASE_SHA" "$CANDIDATE_SHA" \
  --readme README.md --api-pattern 'contracts/*.json' --api-doc docs/api.md \
  --changelog CHANGELOG.md --adr-dir docs/decisions
```

Missing or blank required documents block. An API change without edits to both the reference and changelog blocks. The job also checks ADRs as defined in the linked standard. A reviewer tries the README command and reads the API example and release entry as a caller. Changing a single word in each file satisfies a change detector while leaving an obsolete parameter documented. Line counts and timestamps cannot establish accuracy.
