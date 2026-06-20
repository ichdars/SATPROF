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
    parser.add_argument("--aggregate", type=Path, help="fodler of different benchmarks to be aggregated", action="store")

    return parser


def main(parser: ArgumentParser):

    args = parser.parse_args()

    config = Path(__file__).parent / "config" / "config_tree_cadical.json"

    if args.file:

        steps = read_logfile(args.file)

        with open(config) as f:
            config_tree = json.load(f)
        tree = compare_log_to_config(steps, config_tree)

        dot = Digraph()
        dot.attr(rankdir="TB")

        benchmark: Benchmark = create_benchmark(args.file, config_tree, "a benchmark", "cadical", 4)

        draw_tree(dot, tree, filled=args.filled, root=benchmark.root)

        dot.render("tree", format="png", cleanup=True)
        print("Saved to tree.png")

    if args.aggregate:
        parse_path(args.aggregate)


if __name__ == "__main__":
    parser = build_parser()
    main(parser)
