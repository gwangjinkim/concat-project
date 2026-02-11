# Issue: Flexible file targeting for `--input`, `--ext`, and content grep

## Problem
Users need more flexible ways to select files for concatenation.

Current behavior is limited to:
- a single project root path via `--input`
- simple extension suffix checks via `--ext`

This makes it hard to target mixed file layouts in larger repos.

## Requested behavior
1. `--input` should accept:
   - literal file paths
   - POSIX-style globs
   - regex selectors
2. `--ext` should accept:
   - literal extensions
   - glob-based selectors
   - regex selectors
3. Add `--grep [pattern]` to include only files whose content matches a regex.

## Proposed CLI shape
- Add `--root` (defaults to `.`) as discovery base.
- Make `--input` optional selectors relative to `--root`.
- Keep `--ext` required.
- Add `--grep` with optional regex argument.

## Acceptance criteria
- Literal, glob, and regex matching all work for `--input`.
- Literal, glob, and regex matching all work for `--ext`.
- `--grep` filters by content regex.
- Filtered tree output only includes files that pass all active filters.
