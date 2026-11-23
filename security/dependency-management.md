# Dependency management

Use this standard to select, update and release third-party components. It applies to direct and transitive dependencies that enter the shipped artifact.

## Know what will ship

The author SHOULD record why a direct dependency is needed, how its source and version are selected, and what enters the resolved build. Review lockfile changes and transitive additions. Generate the inventory from the release candidate or its reproducible build. A manifest with a version range alone cannot identify the version inside the artifact.

Before promotion, the release maintainer MUST block an artifact with an unresolved finding in the client's blocking dependency ruleset or an incomplete audit. Run the approved scanner on the resolved inventory for that artifact. Record the artifact digest, scanner version and advisory snapshot with the release evidence so the same inputs can be checked again. Refresh the advisory data for a new release decision.

Require successful scanner execution and the [shared scan gate](../checks/security/scan_gate.py) before promotion. Supply a fresh self-contained SARIF 2.1.0 report from the expected scanner. A clean scan has an explicit empty results list and successful invocation records. Missing evidence, an unexpected driver, an unsuccessful invocation or any returned finding blocks. A trusted adapter can translate native output while preserving execution failure and every finding selected by the blocking ruleset. Keep scanner configuration and the required gate outside the candidate's unilateral control.

```sh
python3 "$STANDARDS/checks/security/scan_gate.py" build/dependencies.sarif --tool "$DEPENDENCY_SCANNER_NAME"
```

## Work a finding to closure

A release candidate contains a transitive image parser at synthetic version 1.2. A blocking advisory matches it. Capture the advisory ID, the path from the direct dependency to the parser, the affected artifact digest and the blocked promotion. The owner examines whether untrusted images reach the parser and prioritizes remediation. Upgrade the direct dependency so its resolved graph uses the fixed version, rebuild, check the new inventory, run the image-processing regression tests, and rerun the audit. Promote the verified digest when the gate clears. The old artifact still carries its original decision.

Reviewers decide whether the inventory covers runtime plugins and which findings belong in the client's blocking ruleset. Counting direct dependencies misses a parser bundled by another library. A clean audit against yesterday's snapshot says nothing about an advisory published today. Record the evidence behind any policy change in its own review. A ticket labeling a live blocking finding “accepted” cannot turn the current scan green.
