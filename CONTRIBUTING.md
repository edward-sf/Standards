# Contributing a standard

Start with a decision someone needs to make in a client project. Open an issue describing the decision, who faces it, a concrete example, and the gap in the existing guidance. For an amendment, link the affected section and describe what a client following it would need to change. The repository owner, @edward-sf, reviews scope and assigns the work to a milestone.

## Write a reviewable standard

Use one Markdown document per topic in the appropriate discipline directory. Start with one top-level heading, a purpose, and a scope. State the rules, then work through an example in which a reader can apply them. Use descriptive headings, fenced code blocks with a language when appropriate, and relative links for other repository documents. Link to the document that owns a rule when another topic depends on it.

| Term | How a contributor uses it |
| --- | --- |
| MUST | A mandatory requirement. Name who acts and what a reviewer can inspect to verify the outcome. |
| SHOULD | A recommendation. A project departing from it records its reason. |
| MAY | An optional practice. Choose it when the example and project context warrant it. |

“Changes must be traceable” leaves a reviewer guessing where to look. Write “The PR author MUST link the change request or describe the problem and intended outcome in the PR body.” A reviewer can now open the PR and determine whether the author supplied that evidence. Apply this test to every mandatory rule, including ones expressed without a keyword.

## Enforce subscribed standards in the client

When a client adopts a standard, it MUST enforce every deterministically checkable requirement at the point where a violation would take effect. The Standards repository supplies and maintains the enforcement scripts. The client runs the shared check against its own change and configuration and uses the result to gate the relevant operation. For a merge rule, for example, a failing check blocks the merge. Agent instructions and self-reported compliance do not satisfy this requirement. Preserve the meaning of SHOULD and MAY when defining a failure condition.

For each new or amended standard, the contributor MUST document the enforcement decision alongside the rule and link the evidence from the proposal PR:

- **What the client can enforce.** Identify the inputs, the condition that passes or fails, the Standards-owned script, and where the client runs it. Demonstrate the check with both a conforming and a violating case. The same inputs and configuration must produce the same decision. A script may use existing tools or platform controls.
- **What still requires judgment.** Enforce the checkable portion. For the remainder, describe the approaches considered, what was tried or examined, and why each approach is non-viable for the actual requirement. Give a counterexample or concrete limitation and state what the reviewer must still decide. Pending implementation is an open enforcement gap.
- **Who accepts the evidence.** Before a new or amended standard is accepted, a Standards maintainer MUST explicitly approve the documented enforcement effort, including the rationale for every uncovered requirement. Record the maintainer's decision and the revision it covers in the Standards PR. An agent's self-review or a client team's acceptance cannot grant this approval.

For example, when a client requires independent PR review, a shared check can compare the author and reviewer identities and verify that approval covers the change being merged. A same-author approval fails that policy. A different reviewer's approval can establish independence. Counting comments, however, cannot establish that the reviewer understood the failure behavior: a single comment can identify a regression, and ten comments can miss it. A proposal relying on human judgment for review quality still needs evidence for its independence check and maintainer approval of the remaining limitation.

## Plan and claim work

The [roadmap](docs/plans/2026-11-17-roadmap.md) links milestones and active plans. Specs own requirements. A milestone plan records task boundaries, files, and acceptance checks when work on that milestone starts. Each task has one GitHub issue with its plan ID in the title, a link to the plan section, and its acceptance criteria. The [project board](https://github.com/users/edward-sf/projects/11) records status.

| Board status | Contributor action |
| --- | --- |
| Backlog | Record proposed or dependent work. Reconcile issues with the milestone plan. |
| Ready | Confirm the plan exists, the issue matches it, and prerequisites have landed. Check existing claims, branches, and PRs before picking it up. |
| In Progress | Identify yourself on the issue and record the branch. Work on one issue per branch from the current milestone head. |
| In Review | Open the issue PR into the milestone branch. Record acceptance evidence and request any review the issue requires. |
| Merged to Milestone | Squash-merge the verified issue PR. Delete its branch and keep the issue open for milestone integration. |
| Done | After the owner's merge into main, verify the issue closed and update the board. |

## Follow one change through both merges

1. Start a milestone from up-to-date `main` on `milestone/m<N>`. Push it and open a draft milestone PR into `main` as soon as there is a change to compare. Associate it with the milestone and project and assign the owner.
2. For example, claim issue #42 and branch `42-document-retries` from the current milestone branch. Write the acceptance check, demonstrate the starting gap, make the change, then run the check again. For prose, capture a worked walkthrough, policy decision, or link check and its result.
3. Target the milestone branch with a PR titled, for example, `docs(review): clarify retry evidence`. Include `Part of #42`, the verification results, any plan deviations, and the self-review against the task. Address blocking comments. If the diff changes, identify affected feedback, refresh the evidence, and review the revision under the applicable approval rules.
4. A contributor or agent can squash-merge the issue PR once applicable checks pass, the task review is recorded, and required approvals are in. Use the PR title as the squash commit subject. Move #42 to Merged to Milestone.
5. Once all milestone issues reach that state, verify the integrated branch against the milestone exit criteria. In the milestone PR, list every issue PR, give a separate `Closes #42` line for each corresponding issue with its actual number, and attach the evidence. Mark the PR ready. Only the owner approves and merges it into `main`, using a merge commit. Verify issue closure and retire the integration branch.

### Hand off an open issue

On the issue or PR, record the issue number, branch, PR link, revision tested, checks and results, remaining feedback, and next action. For example, a handoff on #42 might say that the retry example passed on the linked PR's current commit and the next action is to verify revised wording against the independent-review policy. The incoming contributor checks the live PR head, acknowledges the handoff, and continues on that branch. If it advanced, identify which evidence needs refreshing.

### Exceptions and newly discovered work

- **Owner checkpoint.** Mark the issue as a checkpoint, identify the decision needed, and notify the owner. Dependent work waits for explicit approval. Only the owner closes checkpoint issues.
- **Hotfix.** Track an urgent change outside the milestone in its own issue and open a PR into main for owner review. After it merges, synchronize the active milestone by merging main into it through a PR. Preserve shared branch history.
- **Deviation.** Record implementation changes from the plan on the issue PR. A changed requirement updates the spec in that PR or starts with a separate discussion issue when the decision deserves its own review.
- **New finding.** File a bug or follow-up issue. Resolve blockers before dependent work. Assign deferred findings to a suitable open milestone. When none fits, address them in the current one.
