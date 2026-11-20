# M1 implementation plan

The [milestone spec](../specs/2026-11-19-m1-quality-security-operations-design.md) defines the deliverables and exit criteria. Follow the [contributor guide](../../CONTRIBUTING.md#plan-and-claim-work) to claim a task, record the starting gap and submit an issue PR into `milestone/m1`.

## Work order

After T1 lands, testing (T2), secure development (T3), secrets and dependencies (T4), and documentation (T5) can proceed independently. CI/CD (T6) consumes the testing and security gates. The Definition of Done (T7) brings the evidence together. The final walkthrough (T8) exercises all nine documents against a single sample project.

Each standards task owns the scripts and fixtures for its checkable rules alongside the named Markdown files. Its PR records how a subscribing client runs the check, shows pass and fail cases, explains limitations with concrete evidence, and obtains the maintainer decision on the reviewed revision as described in [Enforce subscribed standards in the client](../../CONTRIBUTING.md#enforce-subscribed-standards-in-the-client).

### M1.T1 Publish the M1 spec and implementation plan

[Issue #20](https://github.com/edward-sf/standards/issues/20). M0 has landed.

Milestone spec and plan under `docs/`, and the M1 link in the roadmap.

**Acceptance check.** Map all nine published paths and all seven exit criteria to tasks. Verify roadmap and plan links, dependencies, and a milestone issue for each task.

### M1.T2 Define testing strategy and coverage

[Issue #21](https://github.com/edward-sf/standards/issues/21). Start after T1.

`quality/testing-strategy.md` (M1-D1) and `quality/test-coverage.md` (M1-D2).

**Acceptance check.** Use a change to an API backed by a datastore to distinguish unit, integration, and end-to-end tests. Cover naming, isolation, mocks, fixtures, dependency boundaries, regression tests, and meaningful assertions. Show how a reviewer detects an untested failure path even when line coverage passes.

### M1.T3 Define secure development requirements

[Issue #22](https://github.com/edward-sf/standards/issues/22). Start after T1.

`security/secure-development.md` (M1-D5).

**Acceptance check.** Walk through a change to an authenticated endpoint that reads a customer's record. Identify authorization, sensitive-data and logging boundaries, secure coding decisions, and triggers for security review. Show what evidence would block a change with missing access checks.

### M1.T4 Define secrets and dependency handling

[Issue #23](https://github.com/edward-sf/standards/issues/23). Start after T1.

`security/secrets-management.md` (M1-D6) and `security/dependency-management.md` (M1-D7).

**Acceptance check.** Trace a credential from provisioning through use and rotation using synthetic examples. Walk a dependency finding from identification through triage, remediation and verification. Show how a client handles a blocked release and records the decision.

### M1.T5 Define project documentation and ADRs

[Issue #24](https://github.com/edward-sf/standards/issues/24). Start after T1.

`documentation/documentation-standards.md` (M1-D8) and `documentation/adr-standards.md` (M1-D9).

**Acceptance check.** Apply README, API reference, inline documentation, changelog, and release-note guidance to one public API change. Contrast a routine edit with a decision warranting an ADR. Demonstrate recording context, alternatives, decision and consequences, then superseding the record.

### M1.T6 Define CI/CD and release gates

[Issue #25](https://github.com/edward-sf/standards/issues/25). Start after T2, T3, T4.

`operations/ci-cd.md` (M1-D4).

**Acceptance check.** Trace a revision through build, test, lint, validation, artifact promotion and deployment environments. Identify the gate, inputs and artifact at each transition. Walk through both a failed pre-deployment check and a failed deployment, including rollback and verification.

### M1.T7 Define objective completion criteria

[Issue #26](https://github.com/edward-sf/standards/issues/26). Start after T2 through T6.

`quality/definition-of-done.md` (M1-D3).

**Acceptance check.** Evaluate the same change for task acceptance, merge and release. Identify the responsible person and evidence for testing, review, documentation and change management. Demonstrate a blocked decision, the missing evidence and the result after correction.

### M1.T8 Publish the catalog and verify a sample project

[Issue #27](https://github.com/edward-sf/standards/issues/27). Start after T7.

`README.md` and the integrated walkthrough in the milestone PR.

**Acceptance check.** Link all nine delivered standards from the catalog. Evaluate a sample project against every milestone exit criterion, recording the client revision, check commands, results, reviewer judgments, and at least one blocked and corrected decision. Link the issue PRs and maintainer approvals from the milestone PR.
