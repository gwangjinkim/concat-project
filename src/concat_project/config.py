import argparse
import re
from pathlib import Path


def _validate_grep_pattern(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        re.compile(value)
    except re.error as exc:
        raise argparse.ArgumentTypeError(f"Invalid regular expression for --grep: {exc}") from exc
    return value


def parse_args():
    parser = argparse.ArgumentParser(description="Concatenate files into a single annotated file.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Root folder used for recursive discovery (default: current directory)",
    )
    parser.add_argument(
        "--input",
        nargs="*",
        default=[],
        help=(
            "File selectors relative to --root. Supports literal paths, POSIX globs "
            "(e.g. src/**/*.py), and regex patterns with the re: prefix."
        ),
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help=(
            "If an --input selector matches a folder, recursively include files within that folder. "
            "Direct file matches are always included."
        ),
    )
    parser.add_argument("--output", required=True, type=Path, help="Output file path")
    parser.add_argument(
        "--ext",
        nargs="+",
        required=True,
        help=(
            "Allowed extension selectors. Supports literals like .py/.lisp, glob patterns, "
            "and regex patterns with re:."
        ),
    )
    parser.add_argument(
        "--grep",
        nargs="?",
        const=".*",
        type=_validate_grep_pattern,
        default=None,
        help=(
            "Only include files whose content matches this regex. If provided without a pattern, "
            "matches any content."
        ),
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help=(
            "Exclude selectors relative to --root. Supports literal paths/prefixes, POSIX globs, "
            "and regex patterns with the re: prefix."
        ),
    )
    parser.add_argument(
        "--exclude-grep",
        nargs="?",
        const=".*",
        type=_validate_grep_pattern,
        default=None,
        help=(
            "Exclude files whose content matches this regex. If provided without a pattern, "
            "excludes any readable text file."
        ),
    )
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files/folders")
    parser.add_argument("--tree-style", default="unicode", choices=["unicode", "ascii"], help="Style of file tree")
    return parser.parse_args()
