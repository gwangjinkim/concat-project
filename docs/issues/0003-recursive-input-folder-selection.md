# Issue: Add `-r/--recursive` for directory matches in `--input`

## Problem
`--input` selectors can match file paths directly, but users also need a controlled way to treat a matched directory as a recursive inclusion root.

## Requested behavior
1. Add `-r` / `--recursive` flag.
2. When enabled and an `--input` selector matches a folder path, include files under that folder recursively.
3. If an `--input` selector matches a file path directly, include that file normally (independent of recursion).
4. Without `--recursive`, folder-only matches should not automatically include nested files.

## Acceptance criteria
- `--input src` + `--recursive` includes files under `src/**`.
- `--input src` without `--recursive` does not include nested files unless they are explicitly matched.
- Literal, glob, and regex selectors continue to work with existing include/exclude and grep filters.
- Final tree output still reflects only files that pass all active filters.
