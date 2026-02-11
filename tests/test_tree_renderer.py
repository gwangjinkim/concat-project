from pathlib import Path

from concat_project.tree_renderer import render_tree


def test_render_tree_contains_only_selected_files():
    tree = render_tree([Path("src/a.lisp"), Path("lib/b.cl")], style="ascii")

    assert "." in tree
    assert "|-- lib" in tree
    assert "|-- src" in tree
    assert "a.lisp" in tree
    assert "b.cl" in tree
