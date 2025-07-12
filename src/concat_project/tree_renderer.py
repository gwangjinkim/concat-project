def render_tree(root, extensions, excludes, include_hidden, style="unicode"):
    lines = []
    charset = {
        "branch": "├── " if style == "unicode" else "|-- ",
        "last":   "└── " if style == "unicode" else "`-- ",
        "pipe":   "│   " if style == "unicode" else "|   ",
        "space":  "    "
    }
    
    def walk(path, prefix=""):
        entries = sorted([e for e in path.iterdir() if e.is_dir() or any(str(e).endswith(ext) for ext in extensions)])
        entries = [e for e in entries if include_hidden or not e.name.startswith(".")]
        entries = [e for e in entries if not any(str(e.relative_to(root)).startswith(x) for x in excludes)]
        
        for i, entry in enumerate(entries):
            connector = charset["last"] if i == len(entries) - 1 else charset["branch"]
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                new_prefix = prefix + (charset["space"] if i == len(entries) - 1 else charset["pipe"])
                walk(entry, new_prefix)
    
    lines.append(".")
    walk(root)
    return "\n".join(lines)
