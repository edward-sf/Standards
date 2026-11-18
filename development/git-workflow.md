# Git workflow

Use this standard to choose and document how changes reach a shared branch and how a release maps to a reviewed revision. It applies to client repositories using Git. The [contributor guide](../CONTRIBUTING.md) defines the particular workflow used to maintain these standards.

## Write a merge policy

The client maintainer MUST publish a merge policy in a contributor guide or other discoverable project document. State the branch names and bases, PR targets, commit convention, permitted merge methods, verification and review requirements, merge authority, and when issues close. Include how a contributor brings a branch up to date and how a releaser identifies the released revision.

Every change needs a traceable purpose and review before merge. A policy can permit a solo maintainer's recorded self-review, require an independent reviewer, or distinguish classes of change. GitHub branch protections can impose additional requirements. Choose a model whose review unit matches the decision the maintainer wants to make.

## Two histories for one change

Suppose issue #42 asks a project to correct its installation command. These illustrative histories each start from a current main branch.

| Step | Short-lived branch | Recommended milestone model |
| --- | --- | --- |
| Branch | Create `42-fix-install` from `main`. | Create `milestone/m2` from `main`. Create `42-fix-install` from the current milestone head. |
| Commit | Use `docs(install): correct the setup command`. The type and scope tell a reader what changed. | Use the same commit convention. Keep the issue branch focused on #42. |
| Open PR | Target `main`; put `Closes #42` in the PR body. | Target `milestone/m2`; put `Part of #42` in the issue PR. Open a draft milestone PR from `milestone/m2` into `main` when there is a diff. |
| Verify and review | Run the published command in a clean checkout. Record the result, inspected diff, and review required by the policy. | Record the same evidence on the issue PR. Resolve review findings and obtain any required checkpoint approval. |
| Merge | The maintainer squash-merges the reviewed PR into the default branch under this example policy. GitHub closes #42. | The contributor squash-merges the verified issue PR with its title as the commit subject. #42 stays open. After integrated checks, the owner reviews the milestone PR with `Closes #42` and merges it using a merge commit. GitHub then closes #42. |

### Review record for the installation fix

In this example client, the guide names `bins/demo` but the executable is at `bin/demo`. The destination directory `installed/` already exists. The author changes one path in the guide and records this PR comment:

> #42, documentation-only. I compared the command with the repository layout. In a fresh checkout the old command failed because `bins/demo` was missing. I ran `install -m 755 bin/demo installed/demo`, then `installed/demo --version`, which printed `demo 1.0`. The diff changes only the documented source path.

Apply **either** review policy to **the same** correction in either branch history above:

- If the client policy permits documentation self-review, the solo maintainer can record that comment and the decision to approve the inspected revision. In the short-lived history the maintainer can then merge into main and close #42. In the milestone history the contributor can squash into the milestone branch; the owner still reviews the milestone PR before #42 closes on main.
- If the client requires independent review, a second maintainer must examine the revised command and evidence and record approval on the change PR. Until then the PR remains open under either history. After approval the same merge authorities, targets, and closure points apply.

The short-lived model works for a project that reviews each change at its default branch. The milestone model lets an owner review a coherent set of changes while agents integrate smaller tasks. In either model the author can name the destination branch, point to the evidence for its current changes, and identify the person authorized to merge.

## Synchronize without disturbing other contributors

Fetch the target branch before starting work and again before integration. When a short-lived branch falls behind main, merge the updated main into it, resolve conflicts, and rerun affected checks. A project can permit rebasing a privately owned branch if its merge policy explains how to coordinate history changes and refresh review evidence.

For an urgent hotfix during milestone M2, branch `57-fix-startup` from current main. Open an owner-reviewed PR back to main for #57. After it merges, open a synchronization PR from main into `milestone/m2`; merge it **with a merge commit** to retain both lines of ancestry. Issue owners then merge the updated milestone into their active branches as needed and repeat affected verification. A shared integration branch keeps its published history.

## Mark a release

Use a tag to identify the exact reviewed revision being released. For example, for a compatible documentation correction to standards release `v1.2.2`, the release owner can tag the reviewed main commit `v1.2.3` after the milestone merge. Verify that the tag resolves to that commit and publish it as part of the release. This is an example tag. The [roadmap](../docs/plans/2026-11-17-roadmap.md) assigns the full standards release and migration policy to M4. Client projects document their own release point and tag convention.
