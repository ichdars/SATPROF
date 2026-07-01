from dataclasses import dataclass, field


@dataclass
class ProfilingNode:
    name: str
    lvl: int
    time: float = 0.0
    percentage: float = 0.0
    color: str = "blue"
    children: list["ProfilingNode"] = field(default_factory=list)


@dataclass
class AggregationNode:
    name: str
    lvl: int
    spread: float
    present_count: int
    total_count: int
    color: str
    time: float = 0.0
    percentage: float = 0.0
    children: list["AggregationNode"] = field(default_factory=list)
    


@dataclass
class SolvingStep:
    name: str
    time: float
    percentage: float


@dataclass
class Benchmark:
    name: str
    solver: str
    profiling_level: int
    root: ProfilingNode
    steps: dict[str, SolvingStep]

@dataclass
class BenchmarkSuite:
    benchmarks: list[Benchmark]
    config: dict


@dataclass
class Outlier:
    min_run: str
    max_run: str
    min_val: float = 0.0
    max_val: float = 0.0


@dataclass
class ProfileMatrix:
    node_order: list[str]
    benchmarks: list[str]
    percent: dict[str, list[float]]
    time: dict[str, list[float]]
    present: dict[str, list[float]]

    def filter_zeros(self, name: str, metric: str = "percent") -> list[float]:
        """ method to filter out all zero values """

        column: list[float] = self.percent[name] if metric == "percent" else self.time[name]
        return [val for val, present in zip(column, self.present[name]) if present]

