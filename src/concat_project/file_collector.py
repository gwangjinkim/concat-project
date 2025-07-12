from pathlib import Path

def collect_files(root: Path, extensions, excludes, include_hidden):
    files = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel_path = path.relative_to(root)
        if not include_hidden and any(part.startswith(".") for part in rel_path.parts):
            continue
        if any(str(rel_path).startswith(e) for e in excludes):
            continue
        if not any(str(path).endswith(ext) for ext in extensions):
            continue
        files.append((rel_path, path))
    return sorted(files)
