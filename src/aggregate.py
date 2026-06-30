from typing import Optional

from .parse import *
import statistics

def dfs_node_name(config: dict) -> list[str]:
    res: list[str] = []
    seen: set[str] = set()
    def step(node: dict):
        current_name = node["name"]
        if current_name in seen:
            return

        seen.add(current_name)
        res.append(current_name)
        
        for child in node.get("children", []):
            step(child)
    step(config)
    return res


def calc_spreading(column: list[float]) -> float:
    if len(column) < 2:
        return 0.0
    s: list[float] = sorted(column)
    quantile_1: float = statistics.median(s[:len(s)//2])
    quantile_3: float = statistics.median(s[(len(s) + 1) // 2:])
    return quantile_3 - quantile_1


def build_matrix(suite: BenchmarkSuite) -> ProfileMatrix:
    node_order: list[str] = dfs_node_name(suite.config)
    percent, time, is_present = {}, {}, {}
    for name in node_order:
        percent[name], time[name], is_present[name] = [], [], []
        for benchmark in suite.benchmarks:
            step = benchmark.steps.get(name)
            percent[name].append(step.percentage if step else 0.0)
            time[name].append(step.time if step else 0.0)
            is_present[name].append(step is not None)
    return ProfileMatrix(node_order, [benchmark.name for benchmark in suite.benchmarks], percent, time, is_present)


def matrix_to_tree(matrix: ProfileMatrix, config: dict, stat: str = "median") -> AggregationNode:

    def build(config_node: dict):
        name: str = config_node["name"]

        time_column: list[float] = matrix.filter_zeros(name, "time")
        percentage_column: list[float] = matrix.filter_zeros(name, "percent")
        median_time: float = statistics.median(time_column) if time_column else 0.0
        median_percentage: float = statistics.median(percentage_column) if percentage_column else 0.0
        spreading: float = calc_spreading(percentage_column)
        children: list[Optional[AggregationNode]] = [build(child) for child in config_node.get("children", [])]

        return AggregationNode(
            name=name,
            lvl=config_node["profiling_lvl"],
            spread=spreading,
            present_count=len([tmp for tmp in matrix.present[name] if tmp]),
            total_count=len(matrix.present[name]),
            color=config_node.get("color", "blue"),
            time=median_time, 
            percentage=median_percentage,
            children=children,
            )
    return build(config)
