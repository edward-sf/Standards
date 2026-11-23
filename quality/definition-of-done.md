# Definition of Done

Use this standard to decide whether a task is complete, whether its revision may merge, and whether the merged revision may ship. Each decision draws on evidence the other standards produce. This document names who supplies and accepts that evidence. It applies to every change that alters a client's shipped behavior, public contract or documentation.

## Decide from evidence on the revision

A client maintainer MUST publish the evidence and approvals required for task acceptance, merge and release in protected policy. A reviewer can then open the policy and the change record and see which item is missing. Evidence counts only for the exact revision under decision. An approval or a passing check on an earlier commit describes code that no longer exists.

Consider issue #58, which makes a second reservation for the same seat return 409, as in the [testing strategy](testing-strategy.md). Dana authors the change, Lee reviews it, and Kim owns the release.

| Area | Task acceptance | Merge | Release |
| --- | --- | --- | --- |
| Testing | Dana maps each acceptance criterion to a passing case, such as `duplicate_seat_returns_conflict`. | CI runs the [report check](../checks/quality/test_reports.py) on the PR head. Lee judges whether the assertions cover the failure path. | The pipeline reruns the checks on the merged revision, as [CI/CD](../operations/ci-cd.md) requires. |
| Review | Lee confirms each criterion's evidence answers the issue. | Lee records the outcome on the head revision under the [review standard](../development/code-review.md). | Kim approves the release of the merged revision. |
| Documentation | Dana updates the API reference and changelog for the new status. | CI runs the [documentation gate](../checks/documentation/docs_gate.py). | Kim publishes release notes drawn from the changelog. |
| Change management | Dana links #58 and records any plan deviation on the PR. | The merger checks base, checks and review as the [PR standard](../development/pull-request-standards.md) requires. | The [promotion gate](../checks/operations/promotion_gate.py) passes and the release is tagged under the [Git workflow](../development/git-workflow.md). |

## Gate each decision

Before acting on a decision, the client MUST run the completion gate on the change record and stop if it fails. The protected pipeline assembles the record from platform data: the author, the revision under decision, each acceptance criterion with the evidence name that satisfies it, the result of each check, and each approval with the reviewer and revision. Keep the policy and the record outside the change's control, as the promotion gate does.

```json
{"roles": {"reviewer": ["lee", "sam"], "release-owner": ["kim"]},
 "decisions": {
   "task": {"criteria": true, "evidence": [], "approvals": {"reviewer": 1}},
   "merge": {"criteria": false, "evidence": ["tests", "docs", "credential-scan"], "approvals": {"reviewer": 1}},
   "release": {"criteria": false, "evidence": ["promotion"], "approvals": {"release-owner": 1}}}}
```

```sh
python3 "$STANDARDS/checks/quality/done_gate.py" policy/done.json build/change-record.json --decision merge
```

The gate passes when the record names a full revision and the latest result on that revision is `pass` for every required evidence item. For task acceptance, every recorded criterion also needs passing evidence, and a record without criteria blocks. Each role needs its configured number of distinct approvers from the role's members on that revision. The author's own approval counts only when the decision sets `"allow_author": true`, such as a solo maintainer's documentation policy. An unknown decision or role, a short revision or a malformed record blocks.

## Block and correct a merge

Lee approves #58 at revision `b1…`. The merge gate fails with `docs: no passing result on this revision` because the documentation gate found the contract changed without a changelog entry. Dana adds the entry and pushes `b2…`. The docs and tests pass on `b2…`, yet the gate now fails with `reviewer: 0 of 1 approval(s) on this revision`. Lee inspects the delta as described in [re-review revised work](../development/code-review.md#re-review-revised-work), confirms the earlier test evidence still applies, and approves `b2…`. The merge gate passes and the merger squash-merges as `c3…`.

For release, the pipeline builds `c3…` and promotes it through staging. The release record names `c3…`, the passing promotion result and Kim's approval on `c3…`. Lee's approval of `b2…` does not satisfy the release role. Kim tags `c3…` once the release gate passes.

## What reviewers still decide

The completion gate proves that named evidence and approvals exist for the revision. It cannot judge whether the acceptance criteria capture what #58 asked for or whether the mapped test exercises each criterion. A criterion pointing at `tests` passes even if no case asserts the 409. Lee decides whether each mapping is credible, and the issue owner decides whether the criteria are complete. An approval proves that an authorized person other than the author acted on the revision, not that they read the failure path. Count-based review metrics cannot establish that either. Plan deviations, ADR need and release-note quality remain reviewer judgments recorded on the PR.
