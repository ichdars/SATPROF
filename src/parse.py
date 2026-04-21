from pathlib import Path
from .models import *


def read_logfile(log: Path):
    with log.open("r", encoding="utf-8") as file:
        root = ProfilingNode("root")
        stack = [root]
        last_time = 0.0

        for line in file:

            if line.startswith("c "):

                partition: list[str] = line.split()

                if len(partition) < 3:

                    continue

                symbol = partition[1]

                try:
                    current_time = float(partition[2])

                except:
                    continue

                time_difference = current_time - last_time
                last_time = current_time

                current_node = stack[-1]
                current_node.time += time_difference
                current_node.calls += 1

                if symbol == "{":
                    tmp_node = ProfilingNode("block")
                    current_node.children.append(tmp_node)
                    stack.append(tmp_node)

                elif symbol == "}":
                    if len(stack) > 1:
                        stack.pop()
                else:
                    node = ProfilingNode(symbol, time=time_difference, calls=1)
                    current_node.children.append(node)

    return root


def print_tree(node: ProfilingNode, indent: int = 0):
    print("  " * indent + f"{node.name} | time={node.time:.4f} | calls={node.calls}")
    for child in node.children:
        print_tree(child, indent + 1)
