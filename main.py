#!/usr/bin/python3
from argparse import ArgumentParser
from pathlib import Path
from src.parse import *
from src.draw import *
from src.build_tree import *
from src.aggregate import *
import json
from graphviz import Digraph

def build_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("--file", type=Path)
    parser.add_argument("--aggregate", type=Path, help="fodler of different benchmarks to be aggregated", action="store")
    parser.add_argument("--solver", type=str, help="folder this benchmark is creatd by")

    return parser


def main(parser: ArgumentParser):

    args = parser.parse_args()

    config = load_configs(Path(__file__).parent / "configs")[args.solver]

    dot = Digraph()
    dot.attr(rankdir="TB")

    save: str = ""

    
    if args.file:

        steps = read_logfile(args.file)

        file_tree = compare_log_to_config(steps, config)

        benchmark: Benchmark = create_benchmark(args.file, config, "a benchmark", "cadical", 4)

        draw_tree(dot, file_tree, root=benchmark.root)

        save = f"{args.file.stem}_{args.solver}_tree"

        dot.render(save, "output/benchmarks", format="png", cleanup=True)
        print(f"Saved to output/benchmarks/{save}.png")


    if args.aggregate:
        suite: BenchmarkSuite = BenchmarkSuite(parse_path(args.aggregate, config), config)
        matrix = build_matrix(suite)

        aggreagtion_tree: AggregationNode = matrix_to_tree(matrix, config)

        outliers = filter_outliers(matrix)

        save = f"{args.aggregate.stem}_{args.solver}_tree"
        save_dir: Path = Path("output/suites") / save
        save_dir.mkdir(parents=True, exist_ok=True)

        draw_tree(dot, aggreagtion_tree, outliers, root=aggreagtion_tree)
        write_outliers(outliers, save_dir / f"{save}_outliers.txt")

        dot.render(save, save_dir, format="png", cleanup=True)

        print(f"Saved to output/suites/{save}.png")

if __name__ == "__main__":
    parser = build_parser()
    main(parser)
