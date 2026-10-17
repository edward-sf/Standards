#!/usr/bin/env bash
# Runs Semgrep at the version pinned in requirements.txt next to this script, passing all
# arguments through. CI and local commands both use it, so there is one version to bump.
#
# Usage: bash semgrep/semgrep.sh --test semgrep/
set -euo pipefail

requirements="$(dirname "${BASH_SOURCE[0]}")/requirements.txt"
version="$(sed -n 's/^semgrep==\([^[:space:]]*\).*/\1/p' "${requirements}")"
[ -n "${version}" ] || { echo "No semgrep==<version> line in ${requirements}" >&2; exit 1; }

exec uvx --from "semgrep==${version}" semgrep "$@"
