# Secrets management

Use this standard when a client introduces, handles or replaces a credential. It covers source changes, runtime delivery and response to exposure.

## Keep credentials out of the change

The service owner SHOULD provision a separately identifiable credential with the narrowest usable permissions, store it in the deployment environment's secret manager, and grant retrieval to the workload identity. Configuration can name the secret reference. The value belongs outside the repository, build output, diagnostics and change record. Prefer short-lived credentials when the provider supports them.

Before merge, the client maintainer MUST block a candidate with a finding from its configured credential scanner or an incomplete scan. Run the scanner over the proposed commit range, including intermediate commits, with the team's approved rules. Scope and rules belong in protected CI configuration. Use an ephemeral checkout and the [scan gate](../checks/security/scan_gate.py). A later deletion from the candidate tree does not erase a value from earlier commits.

```sh
python3 "$STANDARDS/checks/security/scan_gate.py" build/secrets.sarif --tool "$SECRET_SCANNER_NAME"
```

Generate the report in the required job on the candidate, preserving scanner failures. The supported evidence format is a self-contained SARIF 2.1.0 file from one configured driver. Each run contains an explicit results list and at least one successful invocation, with every invocation successful. An empty results list passes. Any result, incomplete invocation, wrong driver or unavailable report blocks. Use a trusted adapter for scanners with a different native format. It must derive invocation success from actual scanner execution and preserve every finding in the configured ruleset. Keep raw reports restricted because snippets may contain the detected secret. The gate prints only counts and structural errors.

## Work through a rotation

Suppose a receipt service uses the synthetic credential reference `receipts/writer` at version A. Issue version B for that service, deliver it through the existing secret reference, roll the workload, and verify a synthetic write under B. Revoke A and verify through the provider that A is inactive. Where safe, verify a synthetic request with A is denied. Record the version identifiers, deployment revision, verification results and timestamps. Keep the credential values out of the ticket.

For a suspected exposure, the owner SHOULD revoke or restrict the exposed credential promptly, investigate its use, and coordinate service restoration with a replacement. Removing a matching line can clear a future scan while the exposed credential remains active. Check provider audit and revocation evidence before closing the incident.

A pattern scanner can flag a synthetic example shaped like a token and miss an opaque value in an unfamiliar format. Resolve a false positive by verifying provenance and narrowly reviewing the scanner configuration. The reviewer inspects runtime access, rotation scope and revocation evidence. A clean source scan cannot observe a provider's access grants or establish containment.

See the [OWASP secrets management guidance](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html).
