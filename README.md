# concat-project

**Concatenate source files from a project into a single file with headers, tree view, and filtering — built for Lisp and beyond.**

---

## Features

- **Recursive directory traversal**
- **Prepends `;;;; filename` before each file's contents**
- **Adds a tree view of the project structure at the top**
- **Filter by file extension (e.g., `.lisp`, `.cl`, `.asd`)**
- **Exclude folders or files**
- **CLI-first, modern `pyproject.toml` setup, zero dependencies**
- **Modular and extensible — clean architecture**

---

## Installation

This project uses [uv](https://github.com/astral-sh/uv) - a next-generation Python package manager that's extremely fast and designed to replace `pip`, `poetry`, `venv`, `virtualenv`, `pyenv`, `pytools`, `pipx`, and more (written in Rust).

### 1. Install uv (if not already)

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

or with Homebrew:

```bash
brew install astral-sh/uv/uv
```

For Windows or other options, see: https://docs.astral.sh/uv/installation/

### 2. Create environment and install

Make sure you're in the root folder of the project.

```bash
uv venv
uv pip install -e .
```
Now the CLI is available:

```bash
concate-project --help
```

---

## Example Usage

```bash
concat-project \
  --input ./my-lisp-project \
  --output ./my-lisp-project/flattened.lisp \
  --ext .lisp .cl .asd \
  --exclude tests .git README.md \
  --tree-style unicode
```

This will:
- Find all .lisp, .cl, .asd files in the folder my-lisp-project
- Skip excluded files or folders like tests/, .git/, and README.md
- Write the output to flattened.lisp, starting with a directory tree
- Prepend each file’s content with a ;;;; filename header

---

##  Command-Line Options

| Option             | Description                                                   |
|--------------------|---------------------------------------------------------------|
| `--input`          | Path to the root project folder (**required**)                |
| `--output`         | Path to write the concatenated file (**required**)            |
| `--ext`            | Allowed file extensions (e.g., `.lisp`, `.cl`, `.asd`)        |
| `--exclude`        | Folders or files to exclude (relative paths)                  |
| `--include-hidden` | Also include hidden files and folders                         |
| `--tree-style`     | Style of file tree: `unicode` (default) or `ascii`            |

---

## Project Layout

```bash
concat-project/
├── pyproject.toml            # CLI configuration
├── README.md
└── src/
    └── concat_project/
        ├── __init__.py
        ├── cli.py             # Entry point
        ├── config.py          # Arg parsing & validation
        ├── tree_renderer.py   # Tree drawing
        ├── file_collector.py  # File discovery
        └── writer.py          # Output generation
```

---

Future Ideas
- `--sort` load-order (ASDF support)
- `--strip-comments` or `--minify`
- `--write-index` of files with byte offsets
- `--output-format` options: plain, JSON, or HTML

---

## For Developers

Want to contribute, extend, or use this in your own tools?
1. Fork it.
2. Create your feature in a separate module in src/concat_project/.
3. Add a test folder if needed.
4. Submit a PR!

---

## License

MIT License.

---

## Inspiration

This tool was originally designed to help analyze large Common Lisp projects like vivace-graph-v3, where organizing and inspecting thousands of lines of code quickly was essential.

---

