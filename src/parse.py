from pathlib import Path
import pathlib
from typing import Iterable, Optional

from .models import *
from .build_tree import *
from .aggregate import build_matrix
import re

SOLVER_BANNER = re.compile(r"^c\s+(\S+)\s+SAT\s+SOLVER", re.IGNORECASE)


def read_logfile(log: Path) -> list[SolvingStep]:
    pattern = re.compile(r"c\s+(\d+\.\d+)\s+(\d+\.\d+)\s*%\s+(\w+)")
    res: list[SolvingStep] = []

    right_block: bool = False
    is_valid_benchmark: bool = False


    with log.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()


            if " profiling " in line:
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

                    percentage = float(match.group(2))

                    name = str(match.group(3))

                    res.append(SolvingStep(name, time, percentage))


        if not is_valid_benchmark:
            raise ValueError(f"didnt find profiling block in {log.stem}")

    return res


def parse_path(folder: Path, config_tree: dict) -> list[Benchmark]:
    res: list[Benchmark] = []
    p = pathlib.Path(folder)
    for log in p.glob("*.log"):
        try:
            benchmark: Benchmark = create_benchmark(log, config_tree, log.stem, config_tree["solver"])
            res.append(benchmark)
        except:
            ValueError()
    return res

def create_benchmark(log_path: Path, config: dict, name: str, solver: str, profiling_lvl: int=2):
    steps: list[SolvingStep] = read_logfile(log_path)
    steps_dict = {s.name: s for s in steps}
    root: ProfilingNode = compare_log_to_config(steps, config)
    return Benchmark(name, solver, profiling_lvl, root, steps_dict)


def load_suite(folder: Path, config: dict) -> tuple[BenchmarkSuite, ProfileMatrix]:
    suite: BenchmarkSuite = BenchmarkSuite(parse_path(folder, config), config)
    return suite, build_matrix(suite)


def detect_solver(log: Path, seen: Iterable[str], max_lines: int = 120) -> Optional[str]:
    solver_names: list[str] = sorted(seen, key=len, reverse=True)

    first: list[str] = []
    start: Optional[int] = None

    with log.open("r", encoding="utf-8", errors="replace") as file:
        for index, line in enumerate(file):
            if index >= max_lines:
                break

            lower_case: str = line.lower()
            first.append(lower_case)

            if "[ banner ]" in lower_case:
                start = len(first)
            
            if " profiling " in lower_case:
                break

            search: list[str] = first[start: ] if first is not None else first

            for line in search:
                for name in solver_names:
                    if name.lower() in line: 
                        return name
        return None


def pick_first_log(folder: Path) -> Optional[Path]:

    if folder.is_file():
        return folder
    return next(folder.glob("*.log"), None)


def pick_config(configs: dict[str, dict], solver: Optional[str], src: Path) -> tuple[dict, str]:

    known: list[str] = sorted(configs.keys())

    if solver:
        if solver not in configs: 
            raise ValueError(f"no valid config for solver {solver}, know: {', '.join(known)}")

        return configs[solver], solver

    log: Optional[Path] = pick_first_log(src)
    if log is None:
        raise ValueError("no valid logfile found in {source}")

    found: Optional[str] = detect_solver(log, known)
    if found is None: 
        raise ValueError(f"could not find a solver from {log.stem}",
                         f"use --solver ( known: { ', '.join(known) })")
    return configs[found], found


def banner_solver(log: Path, max_lines: int = 40) -> Optional[str]:

    with log.open("r", encoding="utf-8", errors="replace") as file:
        for index, line in enumerate(file):
            if index >= max_lines:
                break

            match = SOLVER_BANNER.match(line.strip())

            if match:
                return match.group(1).lower()
        return None

def verify_solver(log: Path, config: dict) -> None:

    expected: str = config["solver"].lower()
    found: Optional[str] = banner_solver(log)

    if found is None:
        print(f"warning: no solvername in {log.stem}, expected: {expected}")
        return 

    if found != expected:
        raise ValueError(f"{log.stem} was produced by {found}, but the config is for {expected}")
        
