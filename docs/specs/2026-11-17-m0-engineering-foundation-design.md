# M0 engineering foundation

This spec defines the first milestone of the engineering standards project. The repository serves engineers, reviewers, and coding agents working across client projects. M0 succeeds when a maintainer can use the published standards to set up a development workflow and a reviewer can use the same documents to decide whether a change is ready to merge.

## Scope in the project

The published milestones define the sequence. M0 establishes engineering principles and the development workflow. M1 adds quality, security, documentation, and operations standards. M2 covers AI engineering. M3 delivers reusable enforcement, templates, and configurations. M4 establishes governance, versioning policy, and ongoing adoption tracking. Each milestone gets a detailed plan when it starts. [Project milestones](https://github.com/edward-sf/standards/milestones)

M0 delivers human-readable Markdown. It documents formatting, static analysis, and release expectations at the level needed to establish a workflow. Shared linter configurations, reusable CI, and release governance belong to their published milestones. The README should distinguish documents available to adopt from the future catalog.

## Approaches

We considered making the AgentOps lifecycle mandatory for every client repository. That would give agents a single branch model, but it would also require a milestone integration branch and a second PR even for projects where one reviewed PR is sufficient.

We chose to require the lifecycle in the standards repository and recommend it to client repositories. The owner values being able to review a coherent milestone while agents integrate smaller issues between those reviews. Clients retain that option and can also satisfy the standard through another documented workflow.

## What a client adopts

Use **MUST** for mandatory requirements, **SHOULD** for recommendations that a project may depart from with a documented reason, and **MAY** for optional practices. Address the person who acts on each requirement. Give enough detail for a reviewer to recognize when it has been met.

Every client MUST document its merge policy, make changes traceable to their purpose, and review changes before merge. A solo maintainer MAY satisfy the review requirement with a self-review when the client's documented merge policy permits it. The author records what they checked and the verification evidence on the PR before merging. If the policy requires an independent reviewer for a class of changes, the PR must receive that review before merge.

For example, a small client can route short-lived branches to its default branch and allow self-review for documentation edits. To fix a broken installation instruction, the maintainer links the PR to the reported problem, runs the corrected command in a fresh checkout, and records the result and what they checked in the diff. A client that needs milestone-level sign-off can adopt the full workflow below.

## M0 deliverables

| ID | File | What a reader must be able to do |
| --- | --- | --- |
| M0-D1 | `README.md` | Identify the owner, audience, and purpose. Find each available standard, understand its requirement levels, and see how to adopt the foundation in a new repository. |
| M0-D2 | `CONTRIBUTING.md` | Propose or update a standard. Follow this repository's planning, issue, branch, review, and merge lifecycle. Find the document structure, terminology, and Markdown conventions to use. |
| M0-D3 | `principles/engineering-principles.md` | Apply simplicity, maintainability, modularity, separation of concerns, and architectural consistency when they pull a decision in different directions. Include a worked trade-off and explain when to record the reasoning. |
| M0-D4 | `development/coding-standards.md` | Evaluate naming, organization, readability, comments, type safety, and error handling. Choose appropriate formatting, linting, and static analysis for the project's language. Label language-specific examples with their scope. |
| M0-D5 | `development/git-workflow.md` | Document a project's branch, commit, synchronization, tagging, and release conventions. Follow a worked branch and commit example for the recommended milestone model and see how another model satisfies the common requirements. Use semantic versioning for standards releases. |
| M0-D6 | `development/pull-request-standards.md` | Prepare a PR with a traceable purpose, reviewable scope, change description, verification evidence, and relevant deviations. Identify its target branch and the conditions for merge. |
| M0-D7 | `development/code-review.md` | Identify who reviews and who may approve a change under the project's merge policy. Evaluate correctness, maintainability, and verification. Give actionable feedback, distinguish blocking findings from suggestions, and resolve blocking findings before merge. |

Each foundational standard states its purpose and scope. For every `MUST`, the contributor identifies the responsible person or role and evidence a reviewer can inspect. For example, a client maintainer documents who can merge, and the reviewer can point to that policy in the client repository. The contribution guide owns this writing convention. Use relative links for repository documents.

After a reviewed PR changes, the author identifies the affected feedback and verification, updates the evidence, and obtains review of the revision under the project's merge policy. The PR standard specifies what the author records. The code review standard specifies who reviews the change and how far that review extends. A spelling correction can receive a focused check of the corrected text. A change that alters behavior or the meaning of a requirement calls for re-review of the affected behavior and fresh verification. The project's existing rules for self-review and independent review apply to both.

## Operating this repository

The spec under `docs/specs/` owns requirements. A roadmap under `docs/plans/` indexes the published milestones and links their plans as they start. The milestone plan under `docs/plans/` will map each task to files, verification, and acceptance criteria. GitHub Issues and the Engineering Standards project board own status. Each issue title starts with its plan task ID, such as `M0.T1`, and its body links to the plan section. The plan may group deliverables that should be reviewed together. Every published deliverable and exit criterion must map to a task. [M0 milestone](https://github.com/edward-sf/standards/milestone/1) · [Standards board](https://github.com/users/edward-sf/projects/11)

1. Start the milestone from current `main` on `milestone/m0`. Publish a draft milestone PR into `main` as soon as the branch has a change for GitHub to compare. Reconcile issues to the plan and move actionable work from `Backlog` to `Ready`.
2. To claim work, record the claim on the issue and move it to `In Progress` before editing. Branch from the current milestone head as `<issue-number>-<short-slug>`. One issue has one working branch. An agent taking over reads the issue, PR, and current branch before continuing.
3. Open the issue PR against `milestone/m0` with a Conventional Commit title, `Part of #<issue>`, verification evidence, and any deviation. Move it to `In Review`. For a documentation task, verify the specified behavior with a worked example, a link check, or a walkthrough tied to the acceptance criteria.
4. An agent may squash-merge an issue PR after applicable checks pass, blocking feedback is resolved, and the agent has recorded a self-review against the task. The owner can reserve an issue for an explicit review checkpoint. Delete the issue branch and move the open issue to `Merged to Milestone`. If `main` advances, merge it into the shared milestone branch to preserve collaborators' history.
5. When all issues reach `Merged to Milestone`, verify the integrated milestone against its exit criteria. List the issue PRs, evidence, and a `Closes #<issue>` entry for each issue in the milestone PR. Mark it ready for the owner's review. The owner reviews and merges it into `main` with a merge commit. Verify closure, move issues to `Done`, and retire the integration branch.

Carry forward the AgentOps exceptions in the contributor guide. Author checkpoints block dependent work until the owner approves. Urgent fixes outside a milestone use a tracked issue and an owner-reviewed PR into `main`. A spec deviation updates the spec or starts a separate discussion issue. Track newly discovered work in an appropriate open milestone and address blocking findings before dependent work proceeds.

Root `AGENTS.md` is the shared entry point for Codex, Claude, and other contributors using agents. It should direct an agent to the contributor guide, the active issue and plan, branch selection, verification, and the owner's merge boundary. Root `CLAUDE.md` imports `AGENTS.md` with `@AGENTS.md`. Both should work in a fresh clone without access to the sibling AgentOps checkout. The contributor guide owns the lifecycle so a workflow change has one place to edit.

## Acceptance

- **Client walkthrough.** Starting at the README, a maintainer of a new project can locate the standards and write a basic merge policy. Walk a sample change through both the short-lived branch example and the recommended milestone model. For each, identify the purpose, branch target, review evidence, and merge authority. In the short-lived branch example, show where the policy permits self-review and where the author recorded the checks and results. Apply the same example to a policy that requires independent review and identify whose review is still needed.
- **Contributor walkthrough.** Starting at either agent entry point, a contributor can find a ready issue, name its branch, identify its PR base, record verification, and hand it to another agent. Follow the issue through both merges and identify where the owner's review occurs.
- **Verifiable requirements.** Inspect each mandatory rule in the foundational standards. A contributor can name who acts and point to the evidence a reviewer could use to determine compliance.
- **Re-review after changes.** Walk a typo correction and a behavior-changing edit through a previously reviewed PR. For each revision, identify affected feedback, verification to repeat, evidence to record, and the reviewer authorized by the project's merge policy.
- **Document review.** Check every M0 deliverable against its published description. Confirm purpose and scope in each standard, consistent requirement levels, practical Git examples, actionable PR and review criteria, and working links from the README and contributor guide.

The plan author may choose task boundaries, examples, and verification commands. Document any decision that changes a client obligation, the owner's review authority, or a published milestone deliverable in the spec before implementation.
