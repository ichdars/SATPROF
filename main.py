#!/usr/bin/python3
from argparse import ArgumentParser
from pathlib import Path
from src.parse import *
from src.draw import *
from src.build_tree import *
from src.aggregate import *
from src.plot import *
import json
from graphviz import Digraph, ExecutableNotFound
import sys


def build_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("--file", type=Path)
    parser.add_argument("--aggregate", type=Path, help="fodler of different benchmarks to be aggregated", action="store")
    parser.add_argument("--solver", type=str, help="folder this benchmark is creatd by")
    parser.add_argument("-o", "--output", type=Path, default=Path("output"), help="Basisverzeichnis für Ausgabedateien (Standard: output/)")
    parser.add_argument("--dist", "-d", action="store_true", help="distribution plot for a benhmarksuite")

    return parser


def main(parser: ArgumentParser):

    args = parser.parse_args()
    if not args.file and not args.aggregate:
        parser.error("either --file or --aggregate is required")
    if args.file and args.aggregate:
        parser.error("--file and --aggregate are mutually exclusive")
    if args.dist and not args.aggregate:
        parser.error("--dist requires --aggregate")

    configs = load_configs(Path(__file__).parent / "configs")
    config, solver = pick_config(configs, args.solver, args.file or args.aggregate)

    first_log = pick_first_log(args.file or args.aggregate)

    if first_log is not None:
        verify_solver(first_log, config)

    base_output: Path = args.output.expanduser()

    dot = Digraph()
    dot.attr(rankdir="TB")

    save: str = ""

    if args.file:

        steps = read_logfile(args.file)

        file_tree = compare_log_to_config(steps, config)

        draw_tree(dot, file_tree, root=file_tree)

        save_dir = base_output / "benchmarks"

        if args.output:
            save_dir = base_output

        save_dir.mkdir(parents=True, exist_ok=True)

        save = f"{args.file.stem}_{solver}_tree"
        dot.render(save, save_dir, format="png", cleanup=True)
        print(f"Saved to {save_dir}/{save}.png")

    if args.aggregate:
        suite: BenchmarkSuite = BenchmarkSuite(parse_path(args.aggregate, config), config)
        matrix = build_matrix(suite)

        aggreagtion_tree: AggregationNode = matrix_to_tree(matrix, config)

        save = f"{args.aggregate.stem}_{solver}_tree"
        save_dir: Path = base_output / "suites" / f"{args.aggregate.stem}_{solver}"
        save_dir.mkdir(parents=True, exist_ok=True)

        if args.dist:
            figure = figure = plot_distributions(
                matrix,
                title=f"{args.aggregate.stem} — {solver}, {len(suite.benchmarks)} benchmarks",
                )
            dist_path = save_dir / f"{args.aggregate.stem}_dist.png"
            figure.savefig(dist_path, dpi=150)  # type: ignore
            plt.close(figure)

        outliers = filter_outliers(matrix)

        draw_tree(dot, aggreagtion_tree, outliers, root=aggreagtion_tree)
        write_outliers(outliers, save_dir / f"{save}_outliers.txt")

        dot.render(save, save_dir, format="png", cleanup=True)

        print(f"Saved to {save_dir}/{save}.png")


if __name__ == "__main__":
    parser = build_parser()
    try:
        main(parser)
    except SatProfError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ExecutableNotFound:
        print("Error: Graphviz executable not found. Please ensure Graphviz is installed and added to your system's PATH.", file=sys.stderr)
