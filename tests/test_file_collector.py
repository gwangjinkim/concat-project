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
