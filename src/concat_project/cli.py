from .config import parse_args
from .file_collector import collect_files
from .tree_renderer import render_tree
from .writer import write_output


def main():
    args = parse_args()
    files = collect_files(
        root=args.root,
        input_selectors=args.input,
        extension_selectors=args.ext,
        excludes=args.exclude,
        include_hidden=args.include_hidden,
        grep_pattern=args.grep,
    )
    tree = render_tree([rel_path for rel_path, _ in files], style=args.tree_style)
    write_output(args.output, args.root, files, tree)
