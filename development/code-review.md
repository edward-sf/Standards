# Code review

Use this standard to decide whether a change is ready to merge. It covers human and agent reviewers of code and documentation. The [PR author](pull-request-standards.md) supplies the purpose, scope, and verification evidence.

## Review the decision and the diff

1. Read the change request and the project's merge policy. Identify the intended base and who may review, approve, and merge this class of change.
2. Trace an ordinary case and a failure or boundary case through the diff. For documentation, try the reader's action and compare the result with the claim. Examine correctness, maintainability, compatibility, and the relevance of the checks.
3. Make feedback actionable. Cite the affected line, describe the consequence, and say what evidence would resolve it. Mark a correctness or unmet-requirement finding as blocking. Label an optional improvement as a suggestion so the author can weigh it.
4. Close the discussion by recording the decision and what you checked. For a blocking finding, inspect the fix or an agreed change of scope before resolving it. When reviewers disagree about the intended behavior, bring the question to the issue owner and keep the finding open.

The authorized reviewer MUST record the review outcome and the basis for it on the PR before merge. A reviewer can approve a verified change, request changes with open findings, or document a policy-permitted self-review. The merge policy identifies who may act on that outcome.

## Worked review: retry documentation

In the [sample PR](pull-request-standards.md#example-pr-document-a-retry-setting), the author documents zero retries and three retries. Check that the initial attempt is separate from the retry count. “This passage says three total attempts, but the check permits four including the initial attempt. Please correct the text and verify the example” is a blocking finding. Shortening the example's heading is a suggestion. Re-read the correction and the reported counts before resolving the finding.

A solo maintainer whose policy permits documentation self-review can record the inspected diff, the zero and three results, and the decision to merge. Under independent review, the second reviewer examines the evidence and records approval. The author cannot satisfy that condition by writing the same comment on their own PR.

## Re-review revised work

| Revision to the reviewed PR | What the authorized reviewer checks |
| --- | --- |
| Typo correction | Inspect the delta since the reviewed revision. If only spelling changed, confirm the rendered sentence and command still carry the same meaning and record that focused check. The earlier retry results still apply. |
| Zero now means unlimited retries | Determine whether the project approved the expanded scope. The earlier zero-case verification is stale. Inspect the bounded scheduler test and compare the revised guide with the implementation. For the three-retry finding, confirm the corrected text still agrees with the positive-limit regression result before carrying its resolution forward. Confirm which reviewer the behavior-change policy requires and record that person's decision on the revision. |

If a revision invalidates earlier evidence, keep the affected finding open until the new evidence supports the result. The author and reviewer can point to a commit, range, or updated diff and the checks they repeated. A new approval should cover what actually changed.
