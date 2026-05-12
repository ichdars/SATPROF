from models import *

def compare_log_to_config(steps: list[SolvingStep], config: dict):
    steps_dict = {step.name: step for step in steps}

    return


def config_to_profling(config_node: dict) -> ProfilingNode:
    config_children: list[ProfilingNode] = []

    for child in config_node["children"]:
        config_to_profling.append(child)

    return ProfilingNode(config_node["name"], config_node["profiling_lvl"], children=config_children)
