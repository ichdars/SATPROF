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
    time: float = 0.0
    percentage: float = 0.0
    color: str = "blue"
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
class ProfileMatrix:
    node_order: list[str]
    benchmarks: list[str]
    percent: dict[str, list[float]]
    time: dict[str, list[float]]
    present: dict[str, list[float]]

