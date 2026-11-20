# Pull request standards

Use this standard as the author or merger of a change. It defines what a reviewer needs to decide whether a proposed change can enter its target branch. The companion [code review standard](code-review.md) covers the review decision.

## Prepare a change for review

The PR author MUST link the change request or describe the problem and intended outcome in the PR body. Use a title that describes the result. Choose the base branch from the project's [merge policy](git-workflow.md). Group edits that need to be accepted together and move unrelated cleanup into another change.

Describe the scope, affected users or interfaces, verification method and results, and any deviation from the plan. Identify open decisions and the person whose review is needed. Give the reviewer enough detail to reproduce a meaningful check on the revision they are reviewing.

## Example PR: document a retry setting

| Field | Author's entry |
| --- | --- |
| Title and target | `docs(config): explain the retry limit`. Branch `42-document-retries` targets `main` under the client's short-lived branch policy. |
| Purpose | #42 reports that operators cannot tell whether zero disables retries. |
| Scope | Document the existing meaning of zero and give one example with three retries. |
| Verification | Compared the guide with the current parser and ran the example with zero and three. Zero scheduled no retries and three allowed up to three retries after the initial attempt. |
| Deviation | None. The parser and default setting keep their existing behavior. |

Under a policy permitting a solo maintainer to self-review documentation, the author records the diff inspected and these verification results on the PR. Under a policy requiring independent review, the author submits the same evidence and waits for an authorized second reviewer to record their decision. A self-review can be a written PR comment. If branch protections require another person's approval, that approval is still needed.

## When the reviewed change moves

The author MUST record which feedback and verification a revision affects, refresh that evidence, and obtain review of the revised change under the project's policy. The PR discussion or review history shows the revised diff, results, and reviewer.

| Edit after review | Author's next step in the example PR |
| --- | --- |
| Typo in the word “retry” | Point to the edited sentence. Record that its rendered text and the command are correct and the existing behavior evidence still applies. Seek a focused check from the permitted reviewer, including yourself if allowed. |
| Change the parser so zero now means unlimited retries | Flag the change in purpose, scope, and risk. Earlier evidence for zero is stale. Agree the new behavior with the issue owner or split it into its own PR. If retained, test zero with a bounded fake scheduler, test positive limits, update the guide and plan deviation, and obtain the review required for a behavior change. |

Before merge, the person merging MUST verify the PR targets the intended base, applicable checks pass, blocking findings are resolved, and the required reviewer has covered the final changes. The base, check results, and review discussion on the PR provide the evidence. Use the merge method and issue-closing convention in the project's policy.
