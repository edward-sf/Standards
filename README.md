# Standards
A centralized source of truth for how software should be designed, built, tested, secured, documented, and maintained across client repositories.

I use these standards across my own engineering projects. The catalog below links to the practices I use today. The [adoption levels](#how-client-repos-consume-the-standards) explain why I want to move from documentation to automated enforcement, and the [pitfalls](#pitfalls-to-avoid) describe where I think standardization can go too far.

Maintained by Edward Simpson-Fitzgibbon (@edward-sf).

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

## Repo structure

Standards are organized around engineering disciplines, remaining language agnostic at the top level.

The following structure is an aspirational example, not a current state representation of the standards as they exist today.

```
engineering-standards/
├── principles/
│   ├── engineering-principles.md
│   ├── design-principles.md
│   └── decision-making.md
│
├── architecture/
│   ├── architecture-principles.md
│   ├── service-design.md
│   ├── api-design.md
│   └── adr-standards.md
│
├── development/
│   ├── coding-standards.md
│   ├── git-workflow.md
│   ├── code-review.md
│   └── pull-request-standards.md
│
├── quality/
│   ├── testing-strategy.md
│   ├── test-coverage.md
│   ├── code-quality.md
│   └── definition-of-done.md
│
├── security/
│   ├── secure-development.md
│   ├── secrets-management.md
│   ├── dependency-management.md
│   └── vulnerability-management.md
│
├── operations/
│   ├── ci-cd.md
│   ├── observability.md
│   ├── logging.md
│   └── release-management.md
│
├── documentation/
│   ├── documentation-standards.md
│   ├── readme-template.md
│   └── adr-template.md
│
├── templates/
│   ├── pull-request-template.md
│   ├── issue-template.md
│   └── repository-template/
│
├── ai-engineering/
│   ├── agent-architecture.md
│   ├── agent-development.md
│   ├── prompt-engineering.md
│   ├── context-management.md
│   ├── tool-integration.md
│   ├── evaluation-standards.md
│   ├── model-selection.md
│   ├── safety-and-guardrails.md
│   ├── observability-and-tracing.md
│   ├── reliability-and-fallbacks.md
│   └── human-in-the-loop.md
│
├── README.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
└── CHANGELOG.md
```

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

Other repos reference the standards repository in their README or CONTRIBUTING documentation.

For example:

```Markdown
## Engineering Standards

This project follows Edward Simpson-Fitzgibbon's [Standards](https://github.com/edward-sf/standards).

Relevant standards:
- Development and coding conventions
- Testing strategy
- Pull request requirements
- Security practices
- Documentation requirements
```

This establishes a common reference, but enforcement is largely dependent on developers and agents to adhere to the standards. In agentic workflows, this is an inefficient way to manage context, increasing the required tool calls and lookups.

A penny-wise, pound-foolish approach that can be cheaply implemented but increases the cost of development overall.

### Level 2 - Templates and shared configurations

The next level of maturity provides reusable assets that projects can adopt.

Examples:
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

This is where the Standards become particularly meaningful.

You can provide reusable GitHub Actions workflows that other repositories call, standardizing your core CI/CD actions across projects cheaply.

**Planned for M3.** The YAML below illustrates how a client repository could call the shared workflow once it is published.

For example:
```YAML
name: Engineering Quality Checks

on:
    pull_request:
    push:
        branches: [main]

jobs:
    quality:
        uses: edward-sf/standards/.github/workflows/quality-checks.yml@v1
```

Your central workflow might enforce:
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

The following mechanisms help to maintain quality engineering standards, which have implications for all client repos. Changes to the standards should be intentional and heavily scrutinized before promotion to `main`.

| Mechanism | Purpose |
| --------- | ------- |
| Semantic versioning | Communicate changes to standards |
| Pull request reviews | Prevent uncontrolled policy changes |
| CODEOWNERS | Define who approves changes |
| Changelog | Track changes and their impact |
| RFC process | Discuss signficiant changes before adoption |
| Deprecation policy | Give projects time to migrate |
| Compliance checks | Identify projects that aren't following standards |

We also distinguish between three tiers of standards:

### Mandatory

Non-negotiable requirements, such as protecting secrets, requiring code reviews, and preventing known critical vulnerabilities from reaching production.

### Recommended

Strong recommendations that projects should follow unless they have a documented reason not to.

### Optional

Suggestions and patterns that teams can adopt depending on their technology, architecture, and circumstances. Primarily used to avoid rework than enforce practices.

## AI Engineering

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
