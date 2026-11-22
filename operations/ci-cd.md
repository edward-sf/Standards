# CI/CD

Use this standard to define how a client revision becomes a deployable artifact, how that artifact moves between environments, and how a team recovers when a check or a deployment fails. It applies to every pipeline that builds or deploys a client artifact into a shared environment. The [Git workflow](../development/git-workflow.md) defines how a revision reaches the release branch and how a release is tagged.

## Build once and trace the artifact

The client maintainer MUST publish the pipeline stages, the environments in promotion order, and the required check for each transition in protected CI configuration. A reviewer can then open the configuration and identify what gates each step.

Build the artifact once from the merged revision in a clean workspace. Identify it by content digest, for example an OCI image `sha256:` digest, and deploy that digest to every environment. A mutable tag such as `latest` can point to a different build between staging and production. Run the remaining checks against the same revision and digest. Merge-time results on a PR head describe a different commit whenever the merge creates one, so rerun the required checks on the merged revision.

Consider the reservation API from the [testing strategy](../quality/testing-strategy.md), merged at revision `a1b2…` and configured with `staging` then `production`.

| Transition | Gate | Inputs | Artifact and evidence |
| --- | --- | --- | --- |
| Merge to release branch | Required PR checks and review from the [review standard](../development/code-review.md) | PR head, protected branch rules | Merged revision `a1b2…` |
| Build | Build command exits successfully | Merged revision, lockfile, pinned build image | Image `sha256:1111…` and its dependency inventory, `build` result |
| Test | Runner exit status and the [report check](../checks/quality/test_reports.py) | Fresh JUnit XML and coverage from `sha256:1111…` | `test` result |
| Lint | Linter exit status | Source at `a1b2…`, protected lint configuration | `lint` result |
| Validate | [Protected-read contract](../checks/security/read_contract.py) and [documentation gate](../checks/documentation/docs_gate.py) | Harness observations and the revision range | `validate` result |
| Security scans | [Scan gate](../checks/security/scan_gate.py) for each scanner | Credential scan of the commit range, dependency audit of the inventory | `credential-scan` and `dependency-audit` results |
| Deploy to staging | [Promotion gate](../checks/operations/promotion_gate.py) | Policy, artifact record, `staging`, `sha256:1111…` | Staging deployment, post-deployment verification |
| Promote to production | Promotion gate | The same record with a verified staging deployment, `production`, `sha256:1111…` | Production deployment, verification, release tag |

## Gate each deployment

Before each deployment to a configured environment, the client's deploy job MUST run the promotion gate and stop if it fails. The policy names the required checks and the environment order. The pipeline appends each check conclusion and each post-deployment verification outcome to the artifact's record. Store the policy and the record where the candidate's own jobs cannot rewrite them, such as protected configuration and an append-only artifact store written by the protected pipeline.

```json
{"checks": ["build", "test", "lint", "validate", "credential-scan", "dependency-audit"],
 "environments": ["staging", "production"]}
```

```sh
python3 "$STANDARDS/checks/operations/promotion_gate.py" policy/promotion.json \
  "build/records/$ARTIFACT_DIGEST.json" --environment production --artifact "$ARTIFACT_DIGEST"
```

The record names one `sha256:` artifact digest and its full source revision. Each check entry names the check, the revision, the artifact and its `conclusion`. Each deployment entry names the environment and `verified` or `failed`. The gate passes when every configured check has a result for that revision and digest and the latest result for each is `success`. The digest being deployed must match the record. The artifact must also be verified in the preceding environment, and its last deployment to the target cannot have failed. A missing result, a stale result from another build, an unknown environment or a malformed record blocks.

## Recover from a failed check

During the reservation release, the dependency audit reruns against fresh advisory data after staging and reports a blocking finding in an image parser. The pipeline appends `dependency-audit: failure` for `sha256:1111…`. The production deploy job runs the promotion gate, which exits with `dependency-audit: latest result is failure`, and the production environment stays on its current release. The owner works the finding as described in [dependency management](../security/dependency-management.md), merges the fix at revision `c3d4…`, and the pipeline builds `sha256:2222…`. That artifact receives its own record and passes the checks and staging before production. The record for `sha256:1111…` keeps the failed result.

## Recover from a failed deployment

The release owner MUST verify each deployment with the client's post-deployment checks before promoting further, and roll back to a previously verified artifact when verification fails. Suppose `sha256:2222…` deploys to production and its synthetic reservation request returns 500 because a production-only configuration value is missing. The deploy job records `production: failed` and redeploys the previous release, `sha256:0000…`. Its record already shows verified staging and production deployments, so the gate allows the rollback. Run the same post-deployment checks against `sha256:0000…` and append the result. Record the incident, both digests and the verification outcomes in the release record.

The gate now blocks a second attempt to deploy `sha256:2222…` to production, because its last production deployment failed. Fix the configuration or the code, build a new artifact and promote it through staging again. Redeploying the same digest after an out-of-band environment repair needs a new record with its own decision.

## What reviewers still decide

The promotion gate decides whether the configured evidence exists for the exact artifact being deployed. It cannot tell whether the configured checks cover the release risk or whether a verification exercises the changed behavior. A smoke test that requests a health endpoint passes while reservations fail. Reviewers decide which post-deployment checks the change needs and which environments must match production for a staging result to count.

Rollback safety needs judgment. If `sha256:2222…` dropped a database column that `sha256:0000…` still reads, the gate permits the rollback because `sha256:0000…` was verified in production earlier, yet the old code fails against the migrated schema. The release owner reviews migrations for backward compatibility before promotion and chooses between rollback and a forward fix during an incident. The gate also trusts the record it is given. A client that lets the candidate's own job write the record or the policy can forge a passing decision. Keep both under the protected pipeline's control and review changes to them separately.
