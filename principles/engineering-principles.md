# Engineering principles

Use these principles when choosing a design or reviewing a change that affects how a system will be maintained. They apply to client projects in any language. A reviewer should be able to explain why the chosen design fits the problem and what would justify revisiting it.

## Questions to ask in a design review

| Principle | Question | Evidence to examine |
| --- | --- | --- |
| Simplicity | What is the smallest design that handles the known requirements and failure cases? | Work through a normal input and a failure. Count the concepts the next maintainer needs to understand both paths. |
| Maintainability | What happens when the next likely requirement changes? | Name the likely edit and the checks that would reveal a regression. |
| Modularity | Can callers use this part through a small, stable boundary? | Inspect its public contract and the dependencies callers inherit. |
| Separation of concerns | Which decisions change for different reasons? | Trace a policy change and an infrastructure change. Each should primarily affect the part responsible for that decision. |
| Architectural consistency | Does the project already solve a similar problem? | Compare the proposed boundary with a nearby implementation and explain material differences. |

The author SHOULD use an established project pattern when it fits the required behavior. If the author chooses a different pattern, record the reason in the PR or design record so the reviewer can assess the trade-off.

## Worked decision: sharing a retry policy

An invoice service and an audit exporter both retry failed requests. A common retry package would remove duplicate loops and align backoff calculations. The invoice service, however, can safely retry only requests with an idempotency key. The exporter can replay a whole batch. A shared retry loop with service-specific switches would couple their release schedules and put invoice safety inside a general-purpose utility.

Keep each operation's retry decision beside its caller. Share the small delay calculation once both callers need the same formula. A pure function taking an attempt count and a cap has a testable boundary, matches the project's existing utilities, and leaves the two failure policies free to change. A reviewer can check that an invoice without a key is attempted once and that a replayable batch still retries.

For a local refactor, the PR can hold that reasoning. If several services will depend on a new package, or reversing the choice will require coordinated migrations, the decision owner SHOULD write an architecture decision record (ADR). Record the context, alternatives, chosen boundary, consequences, and a condition for revisiting it. Here, adoption of a common idempotency contract by both services would justify reconsidering a shared retry loop.
