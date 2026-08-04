#!/usr/bin/python3
from argparse import ArgumentParser
from pathlib import Path
from src.parse import *
from src.draw import *
from src.build_tree import *
from src.aggregate import *
from src.plot import *
import json
from graphviz import Digraph

def build_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("--file", type=Path)
    parser.add_argument("--aggregate", type=Path, help="fodler of different benchmarks to be aggregated", action="store")
    parser.add_argument("--solver", type=str, help="folder this benchmark is creatd by")
    parser.add_argument("--output", "--o", type=Path, default=Path("output"), help="Basisverzeichnis für Ausgabedateien (Standard: output/)")
    parser.add_argument("--dist", action="store_true", help="distribution plot for a benhmarksuite")

    return parser


def main(parser: ArgumentParser):

    args = parser.parse_args()

    configs = load_configs(Path(__file__).parent / "configs")
    config, solver = pick_config(configs, args.solver, args.file or args.aggregate)
    base_output: Path = args.output.expanduser()

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

        save = f"{args.aggregate.stem}_{args.solver}_tree"
        save_dir: Path = base_output / "suites" / save
        save_dir.mkdir(parents=True, exist_ok=True)


        if args.dist:
            figure = plot_distributions(matrix)
            dist_path = save_dir / f"{save}_dist.png"
            figure.savefig(dist_path, dpi=150) # type: ignore
            plt.close(figure)


        outliers = filter_outliers(matrix)

        draw_tree(dot, aggreagtion_tree, outliers, root=aggreagtion_tree)
        write_outliers(outliers, save_dir / f"{save}_outliers.txt")

        dot.render(save, save_dir, format="png", cleanup=True)

        print(f"Saved to {save_dir}/{save}.png")

if __name__ == "__main__":
    parser = build_parser()
    main(parser)
