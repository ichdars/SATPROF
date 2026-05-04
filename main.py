#!/usr/bin/python3
from argparse import ArgumentParser
from pathlib import Path
from src.parse import *
from src.draw import *

def build_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("--file", type=Path)

    return parser


def main(parser: ArgumentParser):

    args = parser.parse_args()

    steps = read_logfile(args.file)

    root = ProfilingNode("solve", steps[-1].time, steps[-1].percentage)

    for children in build_hierarchie(steps[:-1], 0, steps[-1].time)[0]:
        print_tree(children)
    
    dot = tree_to_dot(root)
    dot.render("output", format="svg", view=True)

if __name__ == "__main__":
    parser = build_parser()
    main(parser)
