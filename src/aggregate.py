from .parse import *

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

def build_matrix(suite: BenchmarkSuite) -> ProfileMatrix:
    node_order: list[str] = dfs_node_name(suite.config)
    percent, time, present = {}, {}, {}
    for name in node_order:
        percent[name], time[name], present[name] = [], [], []
        for benchmark in suite.benchmarks:
            step = benchmark.steps.get(name)
            percent[name].append(step.percentage if step else 0.0)
            time[name].append(step.time if step else 0.0)
            present[name].append(step is not None)
    return ProfileMatrix(node_order, [benchmark.name for benchmark in suite.benchmarks], percent, time, present)


