from pathlib import Path

from concat_project.file_collector import collect_files


def _make_file(path: Path, content: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_collect_files_supports_literal_glob_and_regex_selectors(tmp_path: Path):
    _make_file(tmp_path / "src" / "a.lisp", "(defun a ())")
    _make_file(tmp_path / "src" / "b.cl", "(defclass b ())")
    _make_file(tmp_path / "lib" / "c.asd", "(asdf:defsystem :c)")

    files = collect_files(
        root=tmp_path,
        input_selectors=["src/a.lisp", "src/*.cl", "re:^lib/.+\\.asd$"],
        extension_selectors=[".lisp", ".cl", ".asd"],
        excludes=[],
        include_hidden=False,
    )

    assert [str(rel) for rel, _ in files] == ["lib/c.asd", "src/a.lisp", "src/b.cl"]


def test_collect_files_supports_extension_glob_and_regex(tmp_path: Path):
    _make_file(tmp_path / "src" / "one.module.lisp", "(defun one ())")
    _make_file(tmp_path / "src" / "two.module.cl", "(defclass two ())")
    _make_file(tmp_path / "src" / "three.txt", "hello")

    files = collect_files(
        root=tmp_path,
        input_selectors=[],
        extension_selectors=["*.module.*", "re:^src/.*\\.txt$"],
        excludes=[],
        include_hidden=False,
    )

    assert [str(rel) for rel, _ in files] == [
        "src/one.module.lisp",
        "src/three.txt",
        "src/two.module.cl",
    ]


def test_collect_files_applies_grep_filter(tmp_path: Path):
    _make_file(tmp_path / "src" / "match.lisp", "(defun find-me ())")
    _make_file(tmp_path / "src" / "skip.lisp", "(defun other ())")

    files = collect_files(
        root=tmp_path,
        input_selectors=[],
        extension_selectors=[".lisp"],
        excludes=[],
        include_hidden=False,
        grep_pattern="find-me",
    )

    assert [str(rel) for rel, _ in files] == ["src/match.lisp"]


def test_collect_files_supports_exclude_literal_glob_and_regex(tmp_path: Path):
    _make_file(tmp_path / "src" / "keep.lisp", "(defun keep ())")
    _make_file(tmp_path / "src" / "drop.tmp.lisp", "(defun drop1 ())")
    _make_file(tmp_path / "vendor" / "third_party.cl", "(defun drop2 ())")
    _make_file(tmp_path / "archive" / "old.asd", "(defun drop3 ())")

    files = collect_files(
        root=tmp_path,
        input_selectors=[],
        extension_selectors=[".lisp", ".cl", ".asd"],
        excludes=["vendor", "src/*.tmp.lisp", "re:^archive/.*"],
        include_hidden=False,
    )

    assert [str(rel) for rel, _ in files] == ["src/keep.lisp"]


def test_collect_files_applies_exclude_grep_filter(tmp_path: Path):
    _make_file(tmp_path / "src" / "keep.lisp", "(defun keep ())")
    _make_file(tmp_path / "src" / "drop.lisp", "(defun dangerous ())")

    files = collect_files(
        root=tmp_path,
        input_selectors=[],
        extension_selectors=[".lisp"],
        excludes=[],
        include_hidden=False,
        exclude_grep_pattern="dangerous",
    )

    assert [str(rel) for rel, _ in files] == ["src/keep.lisp"]


def test_collect_files_only_takes_direct_file_matches_without_recursive(tmp_path: Path):
    _make_file(tmp_path / "src" / "nested" / "keep.lisp", "(defun keep ())")
    _make_file(tmp_path / "src" / "top.lisp", "(defun top ())")

    files = collect_files(
        root=tmp_path,
        input_selectors=["src"],
        extension_selectors=[".lisp"],
        excludes=[],
        include_hidden=False,
        recursive=False,
    )

    assert [str(rel) for rel, _ in files] == []


def test_collect_files_recurses_when_input_matches_folder(tmp_path: Path):
    _make_file(tmp_path / "src" / "nested" / "keep.lisp", "(defun keep ())")
    _make_file(tmp_path / "src" / "top.lisp", "(defun top ())")
    _make_file(tmp_path / "lib" / "skip.lisp", "(defun skip ())")

    files = collect_files(
        root=tmp_path,
        input_selectors=["src"],
        extension_selectors=[".lisp"],
        excludes=[],
        include_hidden=False,
        recursive=True,
    )

    assert [str(rel) for rel, _ in files] == ["src/nested/keep.lisp", "src/top.lisp"]
