from .config import parse_args
from .file_collector import collect_files
from .tree_renderer import render_tree
from .writer import write_output

def main():
    args = parse_args()
    files = collect_files(args.input, args.ext, args.exclude, args.include_hidden)
    tree = render_tree(args.input, args.ext, args.exclude, args.include_hidden, style = args.tree_style)
    write_output(args.output, args.input, files, tree)

