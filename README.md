# Engineering standards

A centralized source of truth for how software should be designed, built, tested, secured, documented, and maintained across client repositories. Edward Simpson-Fitzgibbon (@edward-sf) maintains this repository for project maintainers, engineers, reviewers, and coding agents.

## Available standards

| Discipline | Use this document to… |
| --- | --- |
| Principles | [Weigh an engineering trade-off](principles/engineering-principles.md) and decide when to record it. |
| Development | [Review code](development/coding-standards.md) for clarity, failure behavior, and language-appropriate checks. |
| Development | [Choose a Git workflow](development/git-workflow.md) and identify branch, commit, merge, and tag conventions. |
| Development | [Prepare a pull request](development/pull-request-standards.md) with purpose, scope, and verification evidence. |
| Development | [Review a change or a revised PR](development/code-review.md) and resolve blocking feedback. |

**MUST** marks a mandatory requirement, **SHOULD** a recommendation a project may depart from with a documented reason, and **MAY** an optional practice.

To change a standard, start with the [contributor guide](CONTRIBUTING.md). Coding agents share the [agent instructions](AGENTS.md). The [roadmap](docs/plans/2026-11-17-roadmap.md) links the milestone plans and future work on quality, security, AI engineering, automation, and governance. The discipline documents above are available for adoption now.

## Adopt the foundation in a new project

Link the relevant standards from your contribution guide. Publish the merge policy and the commands your team uses for verification. For example, a small project's policy could read:

> Branch from current main as `<issue-number>-<short-slug>` and open a PR back to main. Use a Conventional Commit title. Link the issue, describe the intended outcome, and record the checks and results. A maintainer may self-review a documentation-only change by recording the diff inspected and the evidence. Behavior changes require another maintainer's recorded approval. Refresh the affected checks and review after edits. The maintainer squash-merges and uses a closing reference in the PR to close the issue on main. Merge updated main into an active branch before integration when it has fallen behind. The release maintainer tags the reviewed main revision for release using `vMAJOR.MINOR.PATCH`.

Try the policy on a correction to an installation command. Record the problem, run the corrected command in a clean checkout, review the diff under the policy, and merge. A team that wants its owner to review a whole milestone can use the [two worked Git histories](development/git-workflow.md#two-histories-for-one-change) to follow the same correction through an issue PR and a milestone PR.

## Conventions for the standards

- Markdown is used for human-readable standards
- YAML is used for machine-readable policies and configurations
- GitHub Actions are used for automated enforcement
- Semantic versioning is used for releases
- ADRs document significant engineering decisions
- GitHub Issues, Milestones, and Projects are required for planning standards evolution. Pull Requests are required on merges to `main` and to `milestone/**` branches.

## How client repos consume the standards

There are several maturity levels possible.

### Level 1 - Documentation and reference

Other repos reference the standards in their README or contributor guide, as in the adoption example above. The team applies and reviews the rules locally. Targeted links reduce the context that agents need to retrieve.

### Level 2 - Templates and shared configurations

M3 will supply reusable assets that projects can adopt.

Examples include

- Pull request templates
- Issue templates
- CODEOWNERS templates
- EditorConfig
- Linter configurations
- Formatter configurations
- Test configuration examples
- Repository setup templates

For example, a Python project could adopt a common Ruff configuration, while a TypeScript project adopts ESLint conventions. A combination can similarly be adopted.

The standards repository defines the expectations; individual projects implement the appropriate tooling. This helps centralize the standards, but requires local setup for client repos.

### Level 3 - Automated enforcement

M3 will provide reusable GitHub Actions workflows that client repositories can call. Each client will be able to add jobs specific to its stack.

A central workflow can check the following.

- Required tests
- Linting
- Formatting
- Dependency vulnerability scanning
- Secret scanning
- Code quality checks

This avoids maintaining nearly identical CI/CD workflows across multiple projects, while allowing individual client repos to expand on their individual jobs.

Standards should be automated wherever possible. Documentation tells developers what to do; automation helps *ensure* that it actually happens.

## How standards are governed

Standards should be treated as controlled engineering assets.

Changes to the standards receive PR review before promotion to `main`. The roadmap places shared compliance checks in M3 and formal release, change management, and deprecation policies in M4. These mechanisms serve the following purposes.

| Mechanism | Purpose |
| --------- | ------- |
| Semantic versioning | Communicate changes to standards |
| Pull request reviews | Prevent uncontrolled policy changes |
| CODEOWNERS | Define who approves changes |
| Changelog | Track changes and their impact |
| RFC process | Discuss significant changes before adoption |
| Deprecation policy | Give projects time to migrate |
| Compliance checks | Identify projects that aren't following standards |

## Planned AI engineering standards

Given the enormous paradigm shift associated with agentic development workflows, standards around AI Engineering are quickly evolving. Powerful, high-velocity tools require well-defined standards if we want them to produce reliable, deterministic output.

Some important principles to establish for this discipline:

| Area | Example standard |
| ---- | ---------------- |
| Agent architecture | Define clear boundaries between agents, tools, and orchestration |
| Prompt engineering | Version and test prompts as engineering artifacts |
| Evaluation | Establish measurable evaluation criteria before deployment |
| Reliability | Implement timeouts, retries, and fallback strategies |
| Safety | Validate tool permissions and constrain agent actions |
| Observability | Record traces, model usage, latency, and token consumption |
| Context management | Define context limits, retrieval strategies, and provenance |
| Human oversight | Establish approval requirements for consequential actions |

A `harness-engineering.md` standard should cover execution environments, agent permissions, feedback loops, test infrastructure, and automated verification.

## Pitfalls to avoid

A few mistakes worth avoiding:

1. **Overengineering the standards.** Don't write 50 documents before building anything that needs them.
2. **Confusing standards with implementation.** Define what a project must achieve without forcing every project to use the same technology.
3. **Creating rules nobody enforces.** Automate requirements where practical.
4. **Allowing standards to become stale.** Review them periodically and update them based on actual engineering experience.
5. **Making every requirement mandatory.** Distinguish genuine security and quality requirements from preferences.
6. **Creating a central bottleneck.** Make standards changes reviewable and collaborative rather than requiring a central approval for every implementation decision.
