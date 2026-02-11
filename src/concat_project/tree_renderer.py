from pathlib import Path


def render_tree(file_paths: list[Path], style: str = "unicode") -> str:
    lines: list[str] = ["."]
    if not file_paths:
        return "\n".join(lines)

    charset = {
        "branch": "├── " if style == "unicode" else "|-- ",
        "last": "└── " if style == "unicode" else "`-- ",
        "pipe": "│   " if style == "unicode" else "|   ",
        "space": "    ",
    }

    tree: dict[str, dict] = {}
    for file_path in sorted(file_paths):
        current = tree
        for part in file_path.parts:
            current = current.setdefault(part, {})

    def walk(node: dict[str, dict], prefix: str = "") -> None:
        items = sorted(node.items())
        for idx, (name, children) in enumerate(items):
            connector = charset["last"] if idx == len(items) - 1 else charset["branch"]
            lines.append(f"{prefix}{connector}{name}")
            if children:
                next_prefix = prefix + (charset["space"] if idx == len(items) - 1 else charset["pipe"])
                walk(children, next_prefix)

    walk(tree)
    return "\n".join(lines)
