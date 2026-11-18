# Coding standards

Use this standard to write and review changes that another engineer will need to understand, verify, and maintain. It applies across programming languages. A project chooses the tools and idioms appropriate to its stack.

## Readability and organization

- **Naming.** Use the project's domain vocabulary. Name functions for their action and values for what they represent. Include units when they change interpretation, as in `timeout_seconds`.
- **Boundaries.** Group code by responsibility and give each public interface a clear contract. Keep validation close to the point where external data enters the system. Prefer the existing module layout unless moving a responsibility makes a concrete change easier.
- **Control flow.** Handle invalid inputs explicitly and keep the success path easy to trace. A reviewer should be able to tell which return values represent success and how callers observe failure.
- **Comments.** Explain constraints that survive a rewrite, such as why a retry can duplicate a payment. Express ordinary control flow through the code and its names. Update a comment when the assumption it records changes.
- **Type safety.** Represent distinct states explicitly when the language supports it. Validate untrusted input at runtime even when an internal interface has static types. Test both accepted and rejected values at that boundary.

## Error handling

An author changing a failure path MUST show its observable outcome in a test or reproducible PR example. Handle a specific error where a recovery decision is possible. When propagating an exception, preserve the underlying cause and include the context needed to act on it. A fallback value is appropriate only when the contract defines its meaning.

### Python example: a retry limit

Consider this proposed configuration parser:

```python
def get(x):
    try:
        return int(x)
    except Exception:
        return 0
```

A reviewer cannot tell what `get` reads or what unit it returns. A typo such as `"three"` also silently disables retries, exactly as an intentional zero would. Name the setting, define its range, and let the caller report configuration failure before starting the job.

```python
def parse_retry_limit(raw: str) -> int:
    try:
        limit = int(raw)
    except ValueError as exc:
        raise ValueError("retry limit must be an integer") from exc
    if limit < 0:
        raise ValueError("retry limit must be nonnegative")
    return limit
```

For this string interface, `"0"` disables retries, `"3"` permits three retries, and both `"three"` and `"-1"` raise a configuration error. In a language with explicit result types, the same contract can return a parsed value or a typed error.

## Mechanical checks

The project maintainer SHOULD document the commands for formatting, linting, and applicable static analysis in the project's contribution guide. Select checks that detect distinct problems, record their configuration with the project, and explain any category the stack does not support. An author can run the documented commands on a fresh checkout and include the results in the PR.

For example, a Python project might document `ruff format --check .`, `ruff check .`, and its configured type checker. A compiler-based project might use its formatter, warning checks, and type-checking build. A passing tool run still leaves the reviewer the domain questions above, including whether a default changes the meaning of a failure.
