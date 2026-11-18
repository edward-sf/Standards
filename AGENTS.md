# Working on engineering standards

Read the [roadmap](docs/plans/2026-11-17-roadmap.md) to find the active milestone. For M0, read the [spec](docs/specs/2026-11-17-m0-engineering-foundation-design.md) for requirements and the [plan](docs/plans/2026-11-17-m0-engineering-foundation.md) for the task's files and acceptance checks. The [Standards board](https://github.com/users/edward-sf/projects/11) and [M0 issues](https://github.com/edward-sf/standards/milestone/1) track live work.

## Claim and hand off work

1. Pick a Ready issue. Read its task and existing discussion, check for an active claim or PR, then identify yourself on the issue and move it to In Progress.
2. Branch from the current milestone branch as `<issue-number>-<short-slug>`. For a handoff, continue on the existing issue branch. Record the branch, PR, latest checks, remaining work, and next action on the issue or PR.
3. Verify the task's acceptance criteria. Record the checks, results, deviations, and your self-review on the issue PR. Use a Conventional Commit title, target the milestone branch, include `Part of #<issue>`, and move the issue to In Review.
4. If the reviewed change is revised, identify affected feedback, refresh verification, and review the revision before merge. Resolve blocking feedback and honor owner checkpoints. Agents may squash-merge a passing issue PR into the milestone branch. Keep its issue open at Merged to Milestone.
5. The owner reviews and merges the milestone PR into main with a merge commit. The milestone PR carries closing references for the issues. Verify closure before moving them to Done.

For other lifecycle details, including a hotfix or spec deviation, use the [repository workflow in the M0 spec](docs/specs/2026-11-17-m0-engineering-foundation-design.md#operating-this-repository). Task M0.T2 establishes the contributor guide as the permanent home for that workflow.
