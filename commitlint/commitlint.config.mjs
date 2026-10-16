// Conventional Commits, enforced on every commit in a PR and on the PR title (which becomes the
// squash-merge commit) by the commits job in pr-policy.yml.
export default {
  extends: ["@commitlint/config-conventional"],
  rules: {
    // Bodies and footers carry URLs, logs and trailers; wrapping them helps nobody.
    "body-max-line-length": [0],
    "footer-max-line-length": [0],
  },
};
