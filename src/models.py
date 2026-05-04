from dataclasses import dataclass, field


@dataclass
class ProfilingNode:
    name: str
    time: float = 0.0
    calls: int = 0
    children: list["ProfilingNode"] = field(default_factory=list)


@dataclass
class Benchmark:
    name: str
    solver: str
    profiling_level: int
    root: ProfilingNode | None
    total_runtime: float
    total_memory: float


@dataclass
class SolvingStep:
    name: str
    time: float
    memory: float