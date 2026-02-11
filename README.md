# concat-project

**Concatenate source files from a project into a single file with headers, tree view, and filtering — built for Lisp and beyond.**

## Features

- Recursive directory traversal
- Prepends `;;;; filename` before each file's contents
- Adds a tree view of the selected files at the top
- Flexible file selection with literal paths, glob patterns, and regex selectors
- Extension filtering with literals, glob patterns, or regex selectors
- Path exclusion filtering with literal, glob, and regex selectors
- Optional content include/exclude filtering with `--grep [pattern]` and `--exclude-grep [pattern]`
- CLI-first, modern `pyproject.toml` setup

## Installation

This project uses [uv](https://github.com/astral-sh/uv).

```bash
uv venv
uv sync
```

## Example Usage

```bash
concat-project \
  --root ./my-lisp-project \
  --input 'src/**/*.lisp' 're:^lib/.*\\.cl$' \
  --ext .lisp .cl '*.asd' \
  --grep '(defun|defclass)' \
  --exclude 'vendor/**' 're:^archive/' '*.generated.lisp' \
  --exclude-grep '(TODO_REMOVE|DANGEROUS)' \
  --output ./my-lisp-project/flattened.lisp
```

## Command-Line Options

| Option                    | Description |
|---------------------------|-------------|
| `--root`                  | Root directory used for recursive discovery (defaults to current directory) |
| `--input`                 | Optional file selectors relative to `--root` (literal paths, globs, or `re:<pattern>`) |
| `--output`                | Path to write the concatenated file (**required**) |
| `--ext`                   | Required extension selectors (literals, globs, or `re:<pattern>`) |
| `--grep [pattern]`        | Optional regex to include files by content (`--grep` alone means any content) |
| `--exclude`               | Optional exclude selectors (literal path/prefix, glob, or `re:<pattern>`) |
| `--exclude-grep [pattern]`| Optional regex to exclude files by content (`--exclude-grep` alone excludes any readable text file) |
| `--include-hidden`        | Also include hidden files and folders |
| `--tree-style`            | Style of file tree: `unicode` (default) or `ascii` |

## Selector rules

- **Literal path:** `--input src/core/main.lisp`
- **Glob path:** `--input 'src/**/*.lisp'`
- **Regex path:** `--input 're:^src/.+\.lisp$'`
- **Extension literal:** `--ext .lisp cl`
- **Extension glob:** `--ext '*.lisp' '*.cl'`
- **Extension regex:** `--ext 're:\.(lisp|cl|asd)$'`
- **Exclude literal/prefix:** `--exclude vendor`
- **Exclude glob:** `--exclude 'vendor/**' '*.tmp.lisp'`
- **Exclude regex:** `--exclude 're:^archive/'`

## License

MIT License.
