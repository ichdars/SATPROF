from dataclasses import dataclass


@dataclass
class Benchmark:
    name: str
    solver: str
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
    time: str
    calls: str
    children: list["ProfilingNode"]
