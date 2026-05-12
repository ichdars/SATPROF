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

