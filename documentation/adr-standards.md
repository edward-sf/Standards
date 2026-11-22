# Architecture decision records

Use an ADR when a significant choice has viable alternatives and later maintainers will need to understand the trade-off. Examples include changing a public contract, a data model or an operational dependency. Correcting a spelling error in an example can proceed through ordinary review.

## Record the decision

The author SHOULD open the record while alternatives are still under discussion. Use a stable descriptive Markdown filename in the client's dedicated ADR directory. Review the record with the change it governs. Each ADR MUST contain nonempty level-two sections named Status, Context, Alternatives, Decision and Consequences. Status is one line containing Proposed, Accepted, Rejected or Superseded. Record consequences for operators and users, including any migration cost.

For the reservations API, the original record compares offset and cursor pagination. Offset permits random access to a page but can repeat rows when a new reservation arrives. Choosing a cursor makes sequential reads more stable and requires preserving an ordering key. If requirements later demand snapshot consistency, create a new record considering snapshots and their storage cost. Keep the original reasoning accessible. A Superseded record MUST name its successor in a level-two “Superseded by” section containing that record's filename, for example `002-snapshot-pagination.md` as plain text. The successor chain must terminate at an Accepted record.

## Check the record at merge

The [documentation gate](../checks/documentation/docs_gate.py) reads the candidate's Markdown files directly under the configured ADR directory. Reserve that directory for records. It checks the sections, allowed statuses, successor existence and chain termination. The invocation and required job are in the [documentation standard](documentation-standards.md#check-documentation-on-the-candidate-revision). An empty collection is valid before a project makes its first significant decision.

A reviewer still decides whether a change warrants an ADR and whether it seriously considered alternatives. File counts would require records for trivial refactors while missing a one-line compatibility decision. A record listing “cursor” and “offset” with no discussion can pass a heading check. Inspect the consequences for the particular workloads and the decision owner's reasoning during review.
