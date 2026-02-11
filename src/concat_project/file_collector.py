import fnmatch
import re
from pathlib import Path


_REGEX_PREFIX = "re:"


def _is_glob(selector: str) -> bool:
    return any(char in selector for char in "*?[]")


def _matches_single_selector(text: str, selector: str) -> bool:
    if selector.startswith(_REGEX_PREFIX):
        return re.search(selector[len(_REGEX_PREFIX) :], text) is not None
    if _is_glob(selector):
        return fnmatch.fnmatch(text, selector)
    return text == selector


def _matches_selector(text: str, selectors: list[str]) -> bool:
    if not selectors:
        return True
    return any(_matches_single_selector(text, selector) for selector in selectors)


def _matches_input_selector(rel_path: Path, input_selectors: list[str], recursive: bool) -> bool:
    if not input_selectors:
        return True

    rel_path_str = str(rel_path)
    for selector in input_selectors:
        if _matches_single_selector(rel_path_str, selector):
            return True
        if recursive:
            ancestor = rel_path.parent
            while str(ancestor) != ".":
                if _matches_single_selector(str(ancestor), selector):
                    return True
                ancestor = ancestor.parent
    return False


def _is_excluded(rel_path_str: str, exclude_selectors: list[str]) -> bool:
    if not exclude_selectors:
        return False

    for selector in exclude_selectors:
        if selector.startswith(_REGEX_PREFIX):
            if re.search(selector[len(_REGEX_PREFIX) :], rel_path_str):
                return True
        elif _is_glob(selector):
            if fnmatch.fnmatch(rel_path_str, selector):
                return True
        elif rel_path_str == selector or rel_path_str.startswith(selector.rstrip("/") + "/"):
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
        elif _is_glob(selector):
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
    exclude_grep_pattern: str | None = None,
    recursive: bool = False,
):
    files: list[tuple[Path, Path]] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel_path = path.relative_to(root)
        rel_path_str = str(rel_path)

        if not include_hidden and any(part.startswith(".") for part in rel_path.parts):
            continue
        if _is_excluded(rel_path_str, excludes):
            continue
        if not _matches_input_selector(rel_path, input_selectors, recursive):
            continue
        if not _matches_extension(rel_path, extension_selectors):
            continue
        if not _matches_grep(path, grep_pattern):
            continue
        if exclude_grep_pattern is not None and _matches_grep(path, exclude_grep_pattern):
            continue

        files.append((rel_path, path))

    return sorted(files)
