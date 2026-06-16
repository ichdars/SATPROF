#!/usr/bin/python3
from argparse import ArgumentParser
from pathlib import Path
from src.parse import *
from src.draw import *
from src.build_tree import *
import json
from graphviz import Digraph

def build_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("--file", type=Path)
    parser.add_argument("--filled", action="store_true", default=False, help="Falg to control if the nodes ar filled out with color")

    return parser


def main(parser: ArgumentParser):

    args = parser.parse_args()

    steps = read_logfile(args.file)

    config = Path(__file__).parent / "config" / "config_tree.json"

    with open(config) as f:
        config_tree = json.load(f)
    tree = compare_log_to_config(steps, config_tree)

    dot = Digraph()
    dot.attr(rankdir="TB")
    draw_tree(dot, tree, filled=args.filled)

    dot.render("tree", format="png", cleanup=True)
    print("Saved to tree.png")

if __name__ == "__main__":
    parser = build_parser()
    main(parser)
