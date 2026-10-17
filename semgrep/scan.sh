#!/usr/bin/env bash
# Runs the shared Semgrep rules, plus any project rules, over the project in the current directory.
# Called by ci-python.yml. CI only: it deletes the project's .semgrepignore files.
#
# Env:
#   STANDARDS_DIR    checkout of this repo (required)
#   PROJECT_RULES    project rule files or folders, relative to the project, one per line
#   EXCLUDES         extra paths to skip, gitignore syntax, one per line
set -euo pipefail

: "${STANDARDS_DIR:?set STANDARDS_DIR to a checkout of the standards repo}"

# A project's own .semgrepignore could exclude anything, so replace it with the standard one.
while IFS= read -r ignore_file; do
  echo "::warning file=${ignore_file#./}::Ignored ${ignore_file#./}. Use the semgrep-exclude input to skip paths."
  rm "${ignore_file}"
done < <(find . -name .semgrepignore -not -path './.git/*' -not -path './.standards/*')

cp "${STANDARDS_DIR}/semgrep/semgrepignore" .semgrepignore
args=(--config "${STANDARDS_DIR}/semgrep")

while IFS= read -r rules; do
  [ -n "${rules}" ] || continue
  [ -e "${rules}" ] || { echo "::error::semgrep-config path not found: ${rules}"; exit 1; }
  args+=(--config "${rules}")
  # Project rule folders hold their own test fixtures, which must not be scanned.
  printf '/%s\n' "${rules#./}" >> .semgrepignore
done <<< "${PROJECT_RULES:-}"

while IFS= read -r pattern; do
  [ -n "${pattern}" ] && printf '%s\n' "${pattern}" >> .semgrepignore
done <<< "${EXCLUDES:-}"

echo "Effective .semgrepignore:"
sed 's/^/  /' .semgrepignore

# --project-root . anchors the ignore file here and scans every file, not just git-tracked ones.
bash "${STANDARDS_DIR}/semgrep/semgrep.sh" scan "${args[@]}" \
  --project-root . --error --metrics=off --disable-version-check
