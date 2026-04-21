from dataclasses import dataclass, field


@dataclass
class Benchmark:
    name: str
    solver: str
    hierarchie: dict[int, 'SolvingStep']
    total_runtime: float
    total_memory: float


@dataclass
class SolvingStep:
    type: str
    total_time: float
    reductions: int
    total_memory: float
    size: float


@dataclass
class ProfilingNode:
    name: str
    time: float = 0.0
    calls: int = 0
    children: list["ProfilingNode"] = field(default_factory=list)
