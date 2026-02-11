import fnmatch
import re
from pathlib import Path


_REGEX_PREFIX = "re:"


def _matches_selector(text: str, selectors: list[str]) -> bool:
    if not selectors:
        return True

    for selector in selectors:
        if selector.startswith(_REGEX_PREFIX):
            if re.search(selector[len(_REGEX_PREFIX) :], text):
                return True
        elif any(char in selector for char in "*?[]"):
            if fnmatch.fnmatch(text, selector):
                return True
        elif text == selector:
            return True
    return False


def _matches_extension(path: Path, extension_selectors: list[str]) -> bool:
    rel_name = str(path)
    file_name = path.name
    for selector in extension_selectors:
        if selector.startswith(_REGEX_PREFIX):
            pattern = selector[len(_REGEX_PREFIX) :]
            if re.search(pattern, rel_name) or re.search(pattern, file_name):
                return True
        elif any(char in selector for char in "*?[]"):
            if fnmatch.fnmatch(file_name, selector) or fnmatch.fnmatch(rel_name, selector):
                return True
        else:
            normalized = selector if selector.startswith(".") else f".{selector}"
            if file_name.endswith(normalized):
                return True
    return False


def _matches_grep(path: Path, grep_pattern: str | None) -> bool:
    if grep_pattern is None:
        return True

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return re.search(grep_pattern, content, flags=re.MULTILINE) is not None


def collect_files(
    root: Path,
    input_selectors: list[str],
    extension_selectors: list[str],
    excludes: list[str],
    include_hidden: bool,
    grep_pattern: str | None = None,
):
    files: list[tuple[Path, Path]] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel_path = path.relative_to(root)
        rel_path_str = str(rel_path)

        if not include_hidden and any(part.startswith(".") for part in rel_path.parts):
            continue
        if any(rel_path_str.startswith(excluded) for excluded in excludes):
            continue
        if not _matches_selector(rel_path_str, input_selectors):
            continue
        if not _matches_extension(rel_path, extension_selectors):
            continue
        if not _matches_grep(path, grep_pattern):
            continue

        files.append((rel_path, path))

    return sorted(files)
