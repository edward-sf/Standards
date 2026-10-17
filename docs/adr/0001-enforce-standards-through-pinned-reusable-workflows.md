# 0001. Enforce standards through pinned reusable workflows

- Status: Accepted
- Date: 2026-10-16
- Release: v1.0.0

## Context

Every project needs the same baseline: lint, type checks, tests, money-handling rules, commit
conventions and a PR checklist. Copying these into each repo drifts, and copied rules can be
edited away by the project they're meant to constrain. Agent guardrails in the Scaffold template
(hooks, permissions) help, but they run on the developer's machine and can't block a merge.

We also want change-management evidence: who changed a rule, why, who reviewed it, and when each
project adopted it.

## Decision

- This repo holds only shared, enforceable pieces: reusable workflows (`on: workflow_call`), the
  Semgrep rules, the commitlint config and the PR checklist. Per-project starting files live in
  Scaffold.
- Projects call the workflows pinned to an **exact** release tag (`@v1.2.0`), never a branch or
  a floating major tag. A floating tag would change a project's checks without a PR in that project.
- The workflows load rules and config from this repo at the commit the project pinned
  (`job.workflow_sha`), so the rules can't drift ahead of the workflow version.
- Each workflow ends in a `required` job that fails unless every check passed. Projects make
  `ci / required` and `policy / required` required checks in their rulesets, so a project only has
  to require two stable check names even as jobs are added.
- Commit and checklist checks (`pr-policy.yml`) are separate from stack CI, because they must
  rerun when the PR description is edited and that shouldn't rerun the test suite.
- Changes land by reviewed PR here, with an ADR when significant, then a semver release.
  Dependabot opens the upgrade PR in each project.

## Consequences

- One place to change a rule, and every project adopts it through a reviewed PR that shows
  whether it passes. The git history, ADRs, releases and upgrade PRs are the audit trail.
- Projects that ignore Dependabot fall behind. That's visible (open upgrade PRs) rather than
  silent, and is the price of not changing a project's checks under it.
- Projects control their own ruff, mypy and pytest configuration in `pyproject.toml`. This repo
  enforces that the checks run and pass, not their strictness. Rules that must not be weakened
  per project belong in Semgrep here. For the same reason, the Semgrep job replaces any project
  `.semgrepignore` with this repo's. Exclusions go through a workflow input in the project's
  `ci.yml`, where they're visible in review.
- This repo is public. A private repo would need a token secret in every project (for Actions
  and, separately, for Dependabot) just to load the rules, and nothing here is secret. Anyone can
  read the rules, which only matters for someone deliberately evading them; review covers that.
