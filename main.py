#!/usr/bin/python3
from argparse import ArgumentParser
from pathlib import Path
from src.parse import *


def build_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("--file", type=Path)

    return parser


def main(parser: ArgumentParser):

    args = parser.parse_args()

    tree = read_logfile(args.file)

    print_tree(tree)


if __name__ == "__main__":
    parser = build_parser()
    main(parser)
