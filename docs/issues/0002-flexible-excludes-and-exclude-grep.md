# Issue: Extend exclusion filters with selector matching and `--exclude-grep`

## Problem
Exclusion currently behaves as simple path-prefix checks, which is too limited for large/mixed repositories.

## Requested behavior
1. `--exclude` should support the same selector types as `--input`:
   - literal paths/prefixes
   - POSIX-style globs
   - regex selectors (`re:<pattern>`)
2. Add `--exclude-grep [pattern]`:
   - content regex exclusion that runs like `--grep`, but removes matching files
   - `--exclude-grep` without a value excludes any readable text file

## Acceptance criteria
- `--exclude` works with literal/glob/regex selectors.
- `--exclude-grep` removes files by content regex.
- `--grep` and `--exclude-grep` can be combined deterministically.
- Tree output includes only final files after all include/exclude filters.
