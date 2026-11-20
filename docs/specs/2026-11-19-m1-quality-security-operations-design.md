# M1 quality, security and operational standards

A client maintainer preparing a release should be able to answer three questions from the change record. What behavior did we verify? Which quality and security risks remain? Which evidence permits us to ship this revision?

The [published milestone](https://github.com/edward-sf/standards/milestone/2) defines nine deliverables. The [implementation plan](../plans/2026-11-19-m1-quality-security-operations.md) assigns their authorship and verification. M1 builds on the existing [review process](../../development/code-review.md) and [Git workflow](../../development/git-workflow.md).

## Deliverables

| ID | Document | Decision it supports |
| --- | --- | --- |
| M1-D1 | `quality/testing-strategy.md` | Choose the test level, dependencies and fixtures for changed behavior and regressions. |
| M1-D2 | `quality/test-coverage.md` | Interpret coverage with assertions and failure-path evidence. |
| M1-D3 | `quality/definition-of-done.md` | Decide whether a task is complete and whether a revision may merge or ship. |
| M1-D4 | `operations/ci-cd.md` | Gate a revision, promote its artifact and recover from a failed deployment. |
| M1-D5 | `security/secure-development.md` | Assess access control, data handling and the need for security review. |
| M1-D6 | `security/secrets-management.md` | Provision, use, rotate and revoke a credential. |
| M1-D7 | `security/dependency-management.md` | Assess a dependency change or finding and verify its disposition. |
| M1-D8 | `documentation/documentation-standards.md` | Identify the project, API and release documentation affected by a change. |
| M1-D9 | `documentation/adr-standards.md` | Decide when to record an architectural decision and how to supersede it. |

## Adoption and evidence

Each discipline document owns its rules. The Definition of Done points to the evidence the other standards produce. A project should be able to apply the standards to its own stack and distinguish automated decisions from decisions requiring a reviewer.

For each standard, follow the [client enforcement requirements](../../CONTRIBUTING.md#enforce-subscribed-standards-in-the-client). Ship the Standards-owned checks needed for its deterministic requirements with the standard. Record the operation each check gates, its inputs and configuration, a conforming and violating case, and what happens at the client when it fails. For an uncovered requirement, record the approaches examined, their limitations and the decision a reviewer still makes. A Standards maintainer explicitly approves that evidence for the reviewed revision before acceptance.

## Exit criteria

| Milestone criterion | Evidence at integration |
| --- | --- |
| Testing covers unit, integration and end-to-end behavior | Apply all three levels to a sample change and identify the failure each catches. |
| Definition of Done gives objective completion requirements | Identify missing evidence, record a blocked decision, then reassess after correction. |
| CI/CD establishes minimum pipeline expectations | Trace checks and an artifact to release and demonstrate what blocks promotion. |
| Security covers secrets, dependencies, authentication and sensitive data | Inspect the sample's evidence for each area and distinguish checked controls from judgment. |
| Project documentation follows consistent expectations | Locate the applicable project, API and release documentation for the change. |
| ADRs give a repeatable decision process | Trace one significant decision from alternatives through adoption and later revision. |
| A sample project can assess its quality and security posture | Record the client revision, commands, results, remaining risks and release decision in the milestone PR. |
