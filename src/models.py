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
class Benchmark:
    name: str
    solver: str
    profiling_level: int
    root: ProfilingNode | None


@dataclass
class SolvingStep:
    name: str
    time: float
    percentage: float