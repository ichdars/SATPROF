from pathlib import Path

from .models import *
import re


def read_logfile(log: Path) -> list[SolvingStep]:
    pattern = re.compile(r"c\s+(\d+\.\d+)\s+(\d+\.\d+)%\s+(\w+)")

    res: list[SolvingStep] = []

    right_block: bool = False
    
    with log.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()


            if "[ run-time profiling ]" in line:
                right_block = True
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

    return res


def build_hierarchie(entries: list[SolvingStep], index: int, parent_time: float) -> tuple[list[ProfilingNode], int]: 

    children: list[ProfilingNode] = []
    time: float = 0.0

    while index < len(entries) and time < parent_time - 0.01:
        entry = entries[index]
        time += entry.time

        index += 1

        child = ProfilingNode(entry.name, entry.time, entry.percentage)

        child.children, index = build_hierarchie(entries, index, entry.time)

        children.append(child)


    return children, index
