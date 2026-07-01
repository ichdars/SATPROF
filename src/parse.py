from pathlib import Path
import pathlib

from .models import *
from .build_tree import *
import re

def read_logfile(log: Path) -> list[SolvingStep]:
    pattern = re.compile(r"c\s+(\d+\.\d+)\s+(\d+\.\d+)%\s+(\w+)")
    res: list[SolvingStep] = []

    right_block: bool = False
    is_valid_benchmark: bool = False


    with log.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()


            if "[ run-time profiling ]" in line:
                right_block = True
                is_valid_benchmark = True
                continue
            
            if "[ statistics ]" in line:
                right_block = False 
                continue

            if right_block:
                match = pattern.search(line)

                if match:

                    time = float(match.group(1))

                    memory = float(match.group(2))

                    name = str(match.group(3))

                    res.append(SolvingStep(name, time, memory))


        if not is_valid_benchmark:
            raise ValueError(f"didnt find profiling block in {log.stem}")

    return res


def parse_path(folder: Path, config_tree: dict) -> list[Benchmark]:
    res: list[Benchmark] = []
    p = pathlib.Path(folder)
    for log in p.glob("*.log"):
        try:
            benchmark: Benchmark = create_benchmark(log, config_tree, log.stem, "cadical")
        except:
            continue
        res.append(benchmark)
    return res

def create_benchmark(log_path: Path, config: dict, name: str, solver: str, profiling_lvl: int=2):
    steps: list[SolvingStep] = read_logfile(log_path)
    steps_dict = {s.name: s for s in steps}
    root: ProfilingNode = compare_log_to_config(steps, config)
    return Benchmark(name, solver, profiling_lvl, root, steps_dict)
