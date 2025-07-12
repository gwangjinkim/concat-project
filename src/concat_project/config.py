import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Concatenate files into a single annotated file.")
    parser.add_argument("--input", required=True, type=Path, help="Root project folder")
    parser.add_argument("--output", required=True, type=Path, help="Output file path")
    parser.add_argument("--ext", nargs="+", required=True, help="Allowed file extensions (e.g., .lisp, .cl)")
    parser.add_argument("--exclude", nargs="*", default=[], help="Relative filders or files to exclude")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden files/folders")
    parser.add_argument("--tree_style", default="unicode", choices=["unicode", "ascii"], help="Style of file tree")
    return parser.parse_args()
