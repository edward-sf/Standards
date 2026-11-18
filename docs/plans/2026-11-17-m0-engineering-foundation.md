# M0 engineering foundation implementation plan

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans to implement one claimed issue at a time. Use the checkboxes during the task and the GitHub project for shared status.

**Goal:** Give a new client project a usable development workflow and give contributors a repeatable way to change the standards.

**Architecture:** The contributor guide owns this repository's lifecycle. Discipline documents own client-facing requirements. The README provides adoption guidance and both agent entry points direct contributors to the same instructions.

**Tech Stack:** Markdown, Git, GitHub Issues, Projects, and pull requests.

**Spec:** [M0 engineering foundation](../specs/2026-11-17-m0-engineering-foundation-design.md)

## Global constraints

- Use MUST, SHOULD, and MAY consistently. For every MUST, name the responsible role and evidence a reviewer can inspect. Give each foundational standard a purpose and scope.
- Clients document a merge policy, trace changes to their purpose, and review them before merge. Recorded self-review is sufficient when their policy permits it.
- Use the issue-to-milestone branch model in this repository. The owner reviews and merges the milestone PR into main. Use relative links for repository documents.
- Keep client obligations language agnostic and label language-specific examples. Shared configurations, reusable automation, and formal waivers belong to later milestones.

## Review focus

| Case | Proof | Task |
| --- | --- | --- |
| An agent takes over an open PR | Either agent entry point leads to the same issue, branch, latest evidence, and next step. | T1, T2 |
| A mandatory requirement sounds reasonable but cannot be checked | The contributor can identify the actor and observable evidence for every MUST. | T2, T7 |
| A solo maintainer encounters a change requiring independent review | The client policy determines when the PR may merge. | T6 |
| An author changes a reviewed PR | Typo and behavioral revisions each receive proportionate verification and review under the merge policy. | T6 |
| A reader follows the README in a fresh clone | All advertised M0 documents exist and the reader can apply them to one sample change. | T7 |

## Files and dependencies

| Task | Files owned | Handoff |
| --- | --- | --- |
| T1 | This plan, its linked spec, the roadmap, `AGENTS.md`, `CLAUDE.md` | Planning and agent entry points for all tasks |
| T2 | `CONTRIBUTING.md`, agent guide's contributor-guide link | Contributor lifecycle and authoring convention (M0-D2) |
| T3 | `principles/engineering-principles.md` | Engineering trade-offs (M0-D3) |
| T4 | `development/coding-standards.md` | Language-agnostic coding criteria (M0-D4) |
| T5 | `development/git-workflow.md` | Branch, commit, integration, and release examples (M0-D5) |
| T6 | `development/pull-request-standards.md`, `development/code-review.md` | Author and reviewer procedures (M0-D6, M0-D7) |
| T7 | `README.md` | Navigation, adoption, and integrated milestone walkthroughs (M0-D1) |

T2 through T6 can start after T1 lands. T7 integrates their published documents. For each task, claim the corresponding issue, reproduce the missing outcome against the starting branch, and record the results of the acceptance checks on the issue PR. Stage the named files, run `git diff --cached --check` (expect no output), and commit with the task's suggested title. Use the same title for the issue PR.

### M0.T1 Publish the planning and agent entry points

- [ ] Publish the spec, this plan, and `docs/plans/2026-11-17-roadmap.md` on the planning issue branch.
- [ ] Write `AGENTS.md` with the claim, handoff, review, and merge instructions an agent needs before the contributor guide ships. Make `CLAUDE.md` import it with `@AGENTS.md`.
- [ ] Reconcile the GitHub milestone, one issue per task, and the board. Verify the task IDs, acceptance criteria, and plan links against this plan.
- [ ] Commit as `docs(planning): establish M0 plan and agent instructions`.

**Acceptance criteria**

- The roadmap links the five published milestones and the active plan. All seven M0 deliverables map to tasks.
- Starting from either agent file leads to the same spec, plan, issue board, and branch instructions in a fresh clone.
- Each task has one open M0 issue assigned to the owner and tracked on the Standards board. Its body links its plan section and carries the acceptance criteria.

### M0.T2 Document contributing and verifiable requirements

- [ ] Create `CONTRIBUTING.md` with the proposal path, planning artifacts, project statuses, claim and handoff procedure, issue and milestone PR sequence, merge authority, and the spec's exceptions. Update `AGENTS.md` to link directly to the contributor guide and remove duplicated lifecycle detail.
- [ ] Define the Markdown format for a standard, terminology, relative links, and the MUST/SHOULD/MAY convention. Show how to revise “changes MUST be traceable” into a rule that identifies the PR author and the evidence linking a change to its purpose.
- [ ] Walk one issue from Ready through both merges and test a handoff to another agent before the issue PR merges. Check the contributor can locate the issue, PR, branch, verification evidence, and next action.
- [ ] Commit as `docs(contributing): define the contributor lifecycle`.

**Acceptance criteria**

- A contributor can propose or update a standard, follow the branch and board transitions, and identify who may resolve checkpoints, merge issue PRs, and merge the milestone PR.
- The guide covers hotfixes, synchronization, deviations, and newly discovered work. Starting at either agent file leads to the contributor guide.
- For each MUST, contributors can identify the responsible role and the evidence a reviewer could inspect. A worked example demonstrates both. The guide defines MUST, SHOULD, and MAY and the purpose and scope of each standard.

### M0.T3 Define engineering principles and trade-offs

- [ ] Create `principles/engineering-principles.md` covering simplicity, maintainability, modularity, separation of concerns, and consistency with existing architecture.
- [ ] Walk through one decision where extracting shared behavior improves consistency but adds coupling. State the selected option, reason, and when the decision warrants an ADR.
- [ ] Commit as `docs(principles): define engineering decision criteria`.

**Acceptance criteria**

- A maintainer can apply the five principles to a concrete design choice and explain the trade-off.
- The worked example identifies when to record the decision. The standard states its scope and its mandatory rules identify an actor and inspectable evidence.

### M0.T4 Define language-agnostic coding standards

- [ ] Create `development/coding-standards.md` covering naming, organization, readability, comments, type safety, error handling and exceptions, formatting, linting, and static analysis.
- [ ] Review a sample change that swallows a failure or returns an ambiguous result. Contrast it with an explicit failure path. Show how a project selects and records its language-appropriate checks.
- [ ] Commit as `docs(development): define coding standards`.

**Acceptance criteria**

- A reviewer can use the standard to identify a readability problem and an error-handling problem and explain a satisfactory correction.
- Formatting, linting, static analysis, and type-safety expectations are actionable across languages. Language-specific examples identify where they apply. Each mandatory rule has an actor and inspectable evidence.

### M0.T5 Document Git and release conventions

- [ ] Create `development/git-workflow.md` with the shared merge-policy requirements and two worked branch histories. Include names, bases, commit messages, PR targets, merge methods, and the point of issue closure.
- [ ] Trace a main-branch hotfix during an open milestone, including how collaborators synchronize branches. Include a semantic version tag example and distinguish tagging conventions from the release-governance work in M4.
- [ ] Commit as `docs(development): document Git workflows`.

**Acceptance criteria**

- A reader can follow both a short-lived client branch and the recommended milestone model, from a tracked change to a reviewed merge.
- Examples identify the commit convention, sync direction for an active shared branch, tagging convention, release point, and person authorized to merge. Client projects can identify which choices their own policy controls.

### M0.T6 Define pull request and code review standards

- [ ] Create `development/pull-request-standards.md` for author responsibilities and `development/code-review.md` for reviewer responsibilities. Cross-link them and use one sample PR to demonstrate the handoff.
- [ ] Cover scope, purpose, target, verification, deviations, review criteria, actionable feedback, blocking findings, approval, and merge conditions. Run the sample first under a policy permitting self-review, then under one requiring independent review.
- [ ] Change the reviewed sample twice, once to fix a typo and once to change behavior. For each revision, document affected feedback, updated verification, and review by the person permitted under the merge policy.
- [ ] Commit as `docs(development): define pull request and review standards`.

**Acceptance criteria**

- The sample PR records purpose, reviewable scope, target, evidence, and deviations. A reviewer can assess correctness and maintainability, resolve blocking feedback, and identify who may approve and merge.
- A solo maintainer records what they reviewed and the results when self-review is permitted. Under an independent-review policy the reader can identify the outstanding approval.
- The author identifies feedback and verification affected by a revision and obtains review of the revised change under the project policy. Both documents show their role in a typo correction and a behavior-changing edit, including what evidence is refreshed.

### M0.T7 Publish adoption guidance and verify the foundation

- [ ] Update `README.md` with owner, purpose, audience, an index of available standards by discipline, requirement levels, and a short adoption example. Label future assets and preserve the existing adoption maturity model.
- [ ] Follow each advertised local link from a fresh checkout. Use the example to write a basic client merge policy and trace a change under both branch models.
- [ ] Repeat the contributor walkthrough from each agent entry point. Inspect each mandatory rule in the foundational standards for its actor and evidence. Record the results by deliverable on the PR; resolve gaps with the responsible task owner.
- [ ] Commit as `docs(readme): publish the engineering foundation`.

**Acceptance criteria**

- The README identifies the owner, audience, purpose, repository structure, and available standards. Its local links resolve, and a reader can tell which assets are planned.
- The seven deliverables satisfy the milestone exit criteria. Every foundational standard states its purpose and scope, uses consistent normative language, and gives each MUST a responsible role and inspectable evidence.
- A new client can establish its development workflow from the README. The recorded client and contributor walkthroughs cover branch targets, change purpose, review evidence, issue closure, and the owner's milestone merge.
